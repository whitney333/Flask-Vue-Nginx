import stripe
import os
from models.user_model import Users
from datetime import datetime, timezone


PRICE_MAPPING = {
    os.getenv("STRIPE_PRICE_STARTER_MONTHLY"): {
        "plan": "starter",
        "billing_interval": "monthly"
    },
    os.getenv("STRIPE_PRICE_STARTER_YEARLY"): {
        "plan": "starter",
        "billing_interval": "yearly"
    },
    os.getenv("STRIPE_PRICE_STANDARD_MONTHLY"): {
        "plan": "standard",
        "billing_interval": "monthly"
    },
    os.getenv("STRIPE_PRICE_STANDARD_YEARLY"): {
        "plan": "standard",
        "billing_interval": "yearly"
    },
}

class StripeService:

    @staticmethod
    def create_checkout_session(user, plan, billing_interval):
        price_map = {
            ("starter", "monthly"): os.getenv("STRIPE_PRICE_STARTER_MONTHLY"),
            ("starter", "yearly"): os.getenv("STRIPE_PRICE_STARTER_YEARLY"),
            ("standard", "monthly"): os.getenv("STRIPE_PRICE_STANDARD_MONTHLY"),
            ("standard", "yearly"): os.getenv("STRIPE_PRICE_STANDARD_YEARLY"),
        }
        key = (plan, billing_interval)
        if key not in price_map:
            raise ValueError("Invalid plan or billing interval")

        price_id = price_map[key]

        session = stripe.checkout.Session.create(
            mode="subscription",
            customer_email=user.email,
            client_reference_id=user.firebase_id,
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,
                "quantity": 1
            }],
            success_url=os.getenv("FRONTEND_URL") + "/payment/success",
            cancel_url=os.getenv("FRONTEND_URL") + "/payment/cancel",
            subscription_data={
                "metadata": {
                    "plan": plan,
                    "billing_interval": billing_interval,
                    "firebase_id": user.firebase_id
                }
            }
        )
        print("Price ID for plan:", price_id)
        print("STRIPE KEY:", stripe.api_key[:10], flush=True)
        return session

    @staticmethod
    def handle_checkout_completed(session):
        firebase_id = session.get("client_reference_id")
        customer_id = session.get("customer")
        subscription_id = session.get("subscription")

        subscription = stripe.Subscription.retrieve(subscription_id)

        plan = subscription.metadata.get("plan")
        billing_interval = subscription.metadata.get("billing_interval")

        if not plan or not billing_interval:
            print("[Stripe] subscription metadata missing plan")
            print("subscription.metadata =", subscription.metadata)
            return

        user = Users.objects(firebase_id=firebase_id).first()
        if not user:
            print(f"[Stripe] User not found: {firebase_id}")
            return

        # ---- upgrade user ----
        user.update(
            set__is_premium=True,
            set__plan=plan,
            set__billing_interval=billing_interval,
            set__stripe_customer_id=customer_id,
            set__stripe_subscription_id=subscription_id
        )

        print(f"[Stripe] User {firebase_id} upgraded to {plan} ({billing_interval})")

    @staticmethod
    def handle_subscription_created(subscription):
        """
        update premium_expired_at field
        :param invoice:
        :return:
        """

        customer_id = subscription.get("customer")
        firebase_id = subscription.get("metadata", {}).get("firebase_id")

        # print(subscription)
        # print("subscription.created incoming")
        # print("customer_id:", customer_id)
        # print("firebase_id: ", subscription.get("metadata"))

        if not customer_id:
            print("[Stripe] subscription.created missing customer_id")
            return

        if not firebase_id:
            print("[Stripe] subscription missing firebase_id")
            return

        user = Users.objects(firebase_id=firebase_id).first()
        if not user:
            print("[Stripe] subscription.created user not found")
            return

        # ---- get current_period_end ----
        items = subscription.get("items", {}).get("data", [])
        if not items:
            print("[Stripe] subscription.created items.data empty")
            return

        period_end_ts = items[0].get("current_period_end") or subscription.get("current_period_end")
        if not period_end_ts:
            print("[Stripe] subscription.created missing period_end")
            return

        expired_at = datetime.fromtimestamp(
            period_end_ts,
            tz=timezone.utc).replace(tzinfo=None)

        user.update(
            set__premium_expired_at=expired_at
        )

        print(
            f"[Stripe] subscription.created → "
            f"customer={customer_id}, expires={expired_at}",
            flush=True
        )

    @staticmethod
    def handle_subscription_updated(subscription):
        customer_id = subscription.get("customer")
        if not customer_id:
            return

        items = subscription.get("items", {}).get("data", [])
        if not items:
            return

        price_id = items[0]["price"]["id"]

        mapping = PRICE_MAPPING.get(price_id)
        if not mapping:
            print(f"[Stripe] Unknown price_id: {price_id}")
            return

        user = Users.objects(stripe_customer_id=customer_id).first()
        if not user:
            return

        status = subscription.get("status")
        current_period_end = subscription.get("current_period_end")

        user.update(
            set__plan=mapping["plan"],
            set__billing_interval=mapping["billing_interval"],
            set__stripe_subscription_id=subscription.get("id"),
            set__stripe_price_id=price_id,
            set__premium_expired_at=(
                datetime.fromtimestamp(current_period_end)
                if current_period_end else None
            )
        )

        print(
            f"[Stripe] Subscription synced → "
            f"{mapping['plan']} ({mapping['billing_interval']}), "
            f"status={status}"
        )

    @staticmethod
    def handle_subscription_canceled(subscription):
        """
        downgraded membership
        :param subscription:
        :return:
        """
        customer_id = subscription.get("customer")

        if not customer_id:
            print("[Stripe] Missing customer_id in subscription.deleted")
            return

        user = Users.objects(stripe_customer_id=customer_id).first()
        if not user:
            print(f"[Stripe] User not found for customer: {customer_id}")
            return

        # ---- safety guard ----
        if not user.is_premium:
            print(f"[Stripe] User already free: {customer_id}")
            return

        # ---- downgrade user ----
        user.update(
            set__is_premium=False,
            set__plan="free",
            set__billing_interval=None,
            unset__stripe_subscription_id=1,
            unset__stripe_price_id=1,
            unset__premium_expired_at=1,
            set__stripe_subscription_id=None
        )

        print(f"[Stripe] Subscription canceled for user {user.firebase_id}")

    @staticmethod
    def handle_invoice_payment_succeeded(invoice):
        """
        to continue premium status
        :param invoice:
        :return:
        """
        customer_id = invoice.get("customer")
        subscription_id = invoice.get("subscription")

        if not customer_id or not subscription_id:
            return

        user = Users.objects(stripe_customer_id=customer_id).first()
        if not user:
            return

        sub = stripe.Subscription.retrieve(subscription_id)

        user.update(
            set__is_premium=True,
            set__premium_expired_at=datetime.fromtimestamp(
                sub["current_period_end"]
            )
        )

        print(f"[Stripe] Payment succeeded, extended premium: {customer_id}")

    @staticmethod
    def handle_invoice_payment_failed(invoice):
        """
        if payment failed
        :param invoice:
        :return:
        """
        customer_id = invoice.get("customer")

        if not customer_id:
            return

        user = Users.objects(stripe_customer_id=customer_id).first()
        if not user:
            return

        print(f"[Stripe] Payment failed, premium suspended: {customer_id}")

    @staticmethod
    def create_customer_portal(firebase_id, return_url) -> str:
        """
        Create Stripe Billing Portal session
        """
        user = Users.objects(firebase_id=firebase_id).first()
        if not user:
            raise ValueError("User not found")

        if not user.stripe_customer_id:
            raise ValueError("User has no Stripe customer")

        session = stripe.billing_portal.Session.create(
            customer=user.stripe_customer_id,
            return_url=return_url
        )

        return session.url

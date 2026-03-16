from services.user_service import UserService
import stripe
import os
from models.user_model import Users
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


def _build_price_map():
    return {
        ("starter", "monthly"): os.getenv("STRIPE_PRICE_STARTER_MONTHLY"),
        ("starter", "yearly"): os.getenv("STRIPE_PRICE_STARTER_YEARLY"),
        ("standard", "monthly"): os.getenv("STRIPE_PRICE_STANDARD_MONTHLY"),
        ("standard", "yearly"): os.getenv("STRIPE_PRICE_STANDARD_YEARLY"),
    }


def _build_price_mapping():
    price_map = _build_price_map()
    return {
        price_id: {
            "plan": plan,
            "billing_interval": billing_interval
        }
        for (plan, billing_interval), price_id in price_map.items()
        if price_id
    }


def _to_utc_naive(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).replace(tzinfo=None)


class StripeService:

    @staticmethod
    def create_checkout_session(user, plan, billing_interval):
        price_map = _build_price_map()
        key = (plan, billing_interval)
        if key not in price_map:
            raise ValueError("Invalid plan or billing interval")

        price_id = price_map[key]
        if not price_id:
            raise ValueError("Stripe price id is not configured for this plan")

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
        logger.info(f"Created checkout session for plan: {plan}, price_id: {price_id}")
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
            logger.warning(f"[Stripe] subscription metadata missing plan for subscription {subscription_id}")
            return

        user = Users.objects(firebase_id=firebase_id).first()
        if not user:
            logger.error(f"[Stripe] User NOT FOUND in DB for firebase_id={firebase_id} (customer_id={customer_id}, subscription_id={subscription_id}). Payment succeeded but account linking failed.")
            return

        # ---- upgrade user ----
        user.update(
            set__is_premium=True,
            set__plan=plan,
            set__billing_interval=billing_interval,
            set__stripe_customer_id=customer_id,
            set__stripe_subscription_id=subscription_id
        )

        logger.info(f"[Stripe] User {firebase_id} upgraded to {plan} ({billing_interval})")

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
            logger.warning("[Stripe] subscription.created missing customer_id")
            return

        if not firebase_id:
            logger.warning("[Stripe] subscription missing firebase_id")
            return

        user = Users.objects(firebase_id=firebase_id).first()
        if not user:
            logger.warning("[Stripe] subscription.created user not found")
            return

        # ---- get current_period_end ----
        items = subscription.get("items", {}).get("data", [])
        if not items:
            logger.warning("[Stripe] subscription.created items.data empty")
            return

        period_end_ts = items[0].get("current_period_end") or subscription.get("current_period_end")
        if not period_end_ts:
            logger.warning("[Stripe] subscription.created missing period_end")
            return

        expired_at = _to_utc_naive(period_end_ts)

        user.update(
            set__premium_expired_at=expired_at
        )

        logger.info(
            f"[Stripe] subscription.created → "
            f"customer={customer_id}, expires={expired_at}"
        )

    @staticmethod
    def handle_subscription_updated(subscription):
        """
        upgrade from the starter plan to the standard plan
        :param subscription:
        :return:
        """
        customer_id = subscription.get("customer")
        if not customer_id:
            return

        items = subscription.get("items", {}).get("data", [])
        if not items:
            return

        price_id = items[0]["price"]["id"]

        mapping = _build_price_mapping().get(price_id)
        if not mapping:
            logger.warning(f"[Stripe] Unknown price_id: {price_id}")
            return

        user = Users.objects(stripe_customer_id=customer_id).first()
        if not user:
            return

        status = subscription.get("status")
        current_period_end = subscription.get("current_period_end")
        cancel_at_period_end = subscription.get("cancel_at_period_end", False)

        if cancel_at_period_end:
            # If user clicked "Cancel" and it's set to end at period end,
            # we keep their premium until it actually expires.
            # Stripe will send a 'customer.subscription.deleted' event when it expires.
            user.update(
                set__premium_expired_at=(
                    _to_utc_naive(current_period_end)
                    if current_period_end else None
                )
            )
            logger.info(f"[Stripe] Subscription marked for cancellation → user {user.firebase_id} will remain premium until expiry")
            return

        user.update(
            set__plan=mapping["plan"],
            set__billing_interval=mapping["billing_interval"],
            set__stripe_subscription_id=subscription.get("id"),
            set__stripe_price_id=price_id,
            set__premium_expired_at=(
                _to_utc_naive(current_period_end)
                if current_period_end else None
            )
        )
        user.reload()
        UserService.enforce_artist_limit(user)

        logger.info(
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
            logger.warning("[Stripe] Missing customer_id in subscription.deleted")
            return

        user = Users.objects(stripe_customer_id=customer_id).first()
        if not user:
            logger.warning(f"[Stripe] User not found for customer: {customer_id}")
            return

        # ---- safety guard ----
        if not user.is_premium:
            logger.info(f"[Stripe] User already free: {customer_id}")
            return

        # ---- downgrade user ----
        user.update(
            set__is_premium=False,
            set__plan="free",
            set__billing_interval=None,
            set__stripe_subscription_id=None,
            set__stripe_price_id=None,
            set__premium_expired_at=None
        )
        user.reload()
        UserService.enforce_artist_limit(user)

        logger.info(f"[Stripe] Subscription canceled for user {user.firebase_id}")

    @staticmethod
    def handle_invoice_payment_succeeded(invoice):
        """
        to continue premium status
        :param invoice:
        :return:
        """
        customer_id = invoice.get("customer")
        subscription_id = invoice.get("subscription")

        if not customer_id:
            return

        user = Users.objects(stripe_customer_id=customer_id).first()
        if not user:
            return
        # if no subscription id
        if not subscription_id:
            logger.warning("[Stripe] invoice.payment_succeeded without subscription")
            return

        sub = stripe.Subscription.retrieve(subscription_id)

        if sub.get("status") != "active":
            return

        user.update(
            set__is_premium=True,
            set__premium_expired_at=_to_utc_naive(
                sub["current_period_end"]
            )
        )

        logger.info(f"[Stripe] Payment succeeded, extended premium: {customer_id}")

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

        logger.warning(f"[Stripe] Payment failed, premium suspended: {customer_id}")

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

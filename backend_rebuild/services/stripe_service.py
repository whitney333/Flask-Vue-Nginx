import stripe
import os
from models.user_model import Users


class StripeService:

    @staticmethod
    def create_checkout_session(user, plan):
        price_map = {
            "monthly": os.getenv("STRIPE_PRICE_MONTHLY"),
            "yearly": os.getenv("STRIPE_PRICE_YEARLY")
        }

        if plan not in price_map:
            raise ValueError("Invalid plan")

        # create stripe customer
        if not user.stripe_customer_id:
            customer = stripe.Customer.create(
                email=user.email,
                metadata={
                    "firebase_id": user.firebase_id
                }
            )
            user.update(stripe_customer_id=customer.id)

        session = stripe.checkout.Session.create(
            mode="subscription",
            customer=user.stripe_customer_id,
            payment_method_types=["card"],
            line_items=[{
                "price": price_map[plan],
                "quantity": 1
            }],
            success_url=os.getenv("FRONTEND_URL") + "/payment/success",
            cancel_url=os.getenv("FRONTEND_URL") + "/payment/cancel",
            metadata={
                "firebase_id": user.firebase_id,
                "plan": plan
            }
        )
        print("Price ID for plan:", price_map[plan])
        print("STRIPE KEY:", stripe.api_key[:10], flush=True)
        return session

    @staticmethod
    def handle_checkout_completed(session):
        firebase_id = session.get("metadata", {}).get("firebase_id")
        plan = session.get("metadata", {}).get("plan")
        customer_id = session.get("customer")

        if not firebase_id:
            print("Webhook missing firebase_id")
            return

        customer_id = session.get("customer")
        subscription_id = session.get("subscription")

        if not customer_id or not subscription_id:
            print("[Stripe] Missing customer or subscription id")
            return

        user = Users.objects(firebase_id=firebase_id).first()
        if not user:
            print(f"[Stripe] User not found: {firebase_id}")
            return

        if user.is_premium:
            print(f"[Stripe] User already premium: {firebase_id}")
            return

        # ---- upgrade user ----
        user.update(
            set__is_premium=True,
            set__plan=plan,
            set__stripe_customer_id=customer_id,
            set__stripe_subscription_id=subscription_id
        )

        print(f"[Stripe] User {firebase_id} upgraded to premium ({plan})")


    @staticmethod
    def handle_subscription_canceled(subscription):
        customer_id = subscription.get("customer")
        subscription_id = subscription.get("id")

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
            set__plan=None,
            set__stripe_subscription_id=None
        )

        print(f"[Stripe] Subscription canceled for user {user.firebase_id}")

    @staticmethod
    def create_customer_portal(firebase_id, return_url):
        user = Users.objects(firebase_id=firebase_id).first()
        if not user or not user.stripe_customer_id:
            raise ValueError("User not found or no Stripe customer ID")

        # Stripe Customer Portal
        session = stripe.billing_portal.Session.create(
            customer=user.stripe_customer_id,
            return_url=return_url
        )

        return session.url

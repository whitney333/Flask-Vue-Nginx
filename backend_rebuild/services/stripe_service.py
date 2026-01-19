import stripe
from dotenv import load_dotenv
import os


class StripeService:

    @staticmethod
    def create_checkout_session(user, plan):
        load_dotenv()
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

        return session
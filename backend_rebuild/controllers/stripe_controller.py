from flask import request, jsonify, g
from models.user_model import Users
from services.stripe_service import StripeService
import stripe
import os


class StripeController:
    @staticmethod
    def create_checkout_session():
        user = Users.objects(firebase_id=g.firebase_id).first()
        if not user:
            return jsonify({
                "error": "User not found"
            }), 404

        data = request.get_json() or {}
        plan = data.get("plan")

        if not plan:
            return jsonify({
                "error": "Missing plan"
            }), 400

        try:
            session = StripeService.create_checkout_session(
                user=user,
                plan=plan
            )
        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 400
        except Exception as e:
            return jsonify({
                "error": "Stripe checkout failed",
                "message": str(e)
            }), 500

        return jsonify({
            "checkout_url": session.url
        }), 200

    @staticmethod
    def handle_webhook(payload, sig_header):
        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                os.getenv("STRIPE_WEBHOOK_SECRET")
            )
        except ValueError as e:
            return jsonify({
                "error": "Invalid payload"
            }), 400
        except stripe.error.SignatureVerificationError:
            return jsonify({
                "error": "Invalid signature"
            }), 400

        event_type = event["type"]
        data_object = event["data"]["object"]

        handlers = {
            "checkout.session.completed": StripeService.handle_checkout_completed,
            # get premium expired_at
            "customer.subscription.created": StripeService.handle_subscription_created,
            # for switching plan or continue plan
            # "customer.subscription.updated": StripeService.handle_subscription_updated,
            # subscription cancelled
            "customer.subscription.deleted": StripeService.handle_subscription_canceled
        }
        print("Webhook event type:", event["type"], flush=True)
        handler = handlers.get(event_type)
        if handler:
            handler(data_object)
        else:
            print(f"[Stripe] Unhandled event type: {event_type}")

        return jsonify({
            "status": "success"
        }), 200

    @staticmethod
    def customer_portal():
        try:
            url = StripeService.create_customer_portal(
                firebase_id=g.firebase_id,
                return_url="http://localhost/profile"
            )
            return jsonify({
                "url": url
            })
        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 404
        except Exception as e:
            return jsonify({
                "error": "Failed to create portal session",
                "message": str(e)
            }), 500

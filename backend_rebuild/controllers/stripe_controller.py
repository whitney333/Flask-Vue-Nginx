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
        billing_interval = data.get("billing_interval")

        if not plan or not billing_interval:
            return jsonify({
                "error": "Missing plan or billing_interval"
            }), 400

        try:
            session = StripeService.create_checkout_session(
                user=user,
                plan=plan,
                billing_interval=billing_interval
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
        if not sig_header:
            return jsonify({
                "error": "Missing Stripe-Signature header"
            }), 400

        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        if not webhook_secret:
            return jsonify({
                "error": "STRIPE_WEBHOOK_SECRET is not configured"
            }), 500

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                webhook_secret
            )
        except ValueError:
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
            "customer.subscription.created": StripeService.handle_subscription_created,
            "customer.subscription.updated": StripeService.handle_subscription_updated,
            "customer.subscription.deleted": StripeService.handle_subscription_canceled,
            "invoice.payment_succeeded": StripeService.handle_invoice_payment_succeeded,
            "invoice.payment_failed": StripeService.handle_invoice_payment_failed,
        }
        print("Webhook event type:", event_type, flush=True)

        handler = handlers.get(event_type)
        if not handler:
            print(f"[Stripe] Unhandled event type: {event_type}")
            return jsonify({"status": "ignored"}), 200

        try:
            handler(data_object)
        except Exception as e:
            print(f"[Stripe] Handler error ({event_type}): {str(e)}", flush=True)
            return jsonify({
                "error": "Webhook handler failed"
            }), 500

        return jsonify({
            "status": "success"
        }), 200

    @staticmethod
    def customer_portal():
        frontend_url = os.getenv("FRONTEND_URL")
        if not frontend_url:
            return jsonify({
                "error": "FRONTEND_URL is not configured"
            }), 500

        try:
            url = StripeService.create_customer_portal(
                firebase_id=g.firebase_id,
                return_url=frontend_url + "/profile"
            )
            return jsonify({"url": url}), 200

        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 400

        except Exception as e:
            print("[Stripe] Portal error:", str(e), flush=True)
            return jsonify({
                "error": "Failed to create customer portal"
            }), 500

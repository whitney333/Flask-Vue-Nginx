from flask import request, jsonify, g
from models.user_model import Users
from services.stripe_service import StripeService


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
                "error": "Stripe checkout failed"
            }), 500

        return jsonify({
            "checkout_url": session.url
        }), 200
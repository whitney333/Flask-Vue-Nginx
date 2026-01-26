from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.stripe_controller import StripeController
from libs.utils import auth_required

stripe_bp = Blueprint('stripe', __name__)
stripe_api = Api(stripe_bp)


@stripe_bp.route("/checkout-session", methods=["POST"])
@auth_required
def checkout_session():
    return StripeController.create_checkout_session()

@stripe_bp.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    return StripeController.handle_webhook(payload, sig_header)

@stripe_bp.route("/customer-portal", methods=["POST"])
@auth_required
def customer_portal():
    return StripeController.customer_portal()

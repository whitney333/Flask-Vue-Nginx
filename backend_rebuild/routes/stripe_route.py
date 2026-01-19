from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.stripe_controller import StripeController
from libs.utils import auth_required

stripe_bp = Blueprint('stripe', __name__)
stripe_api = Api(stripe_bp)


@stripe_bp.route("/v1/stripe/checkout-session", methods=["POST"])
@auth_required
def checkout_session():
    return StripeController.create_checkout_session()


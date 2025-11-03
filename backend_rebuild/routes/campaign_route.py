from controllers.campaign_controller import CampaignController
from flask import Blueprint, jsonify, request
from flask_restful import Api
from libs.utils import auth_required

campaign_bp = Blueprint('campaign', __name__)
campaign_api = Api(campaign_bp)

@campaign_bp.route("/v1/create", methods=["POST"])
def create_campaign():
    return CampaignController.create_campaign()

@campaign_bp.route("/v1/read", methods=["GET"])
def get_all_campaign_by_user_id():
    result = CampaignController.get_all_campaign_by_user_id()

    return result

@campaign_bp.route("/v1/cancel/<string:campaign_id>", methods=["PATCH"])
def cancel_campaign(campaign_id):
    result = CampaignController.cancel_campaign(campaign_id)

    return result

@campaign_bp.route("/v1/detail/<string:campaign_id>", methods=["GET"])
def get_per_campaign_detail(campaign_id):
    result = CampaignController.get_per_campaign_by_campaign_id(campaign_id)

    return result

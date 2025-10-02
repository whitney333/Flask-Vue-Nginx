from controllers.campaign_controller import CampaignController
from flask import Blueprint, jsonify, request
from flask_restful import Api
from libs.utils import auth_required

campaign_bp = Blueprint('campaign', __name__)
campaign_api = Api(campaign_bp)

@campaign_bp.route("/v1/create", methods=["POST"])
def create_campaign():
    return CampaignController.create_campaign()

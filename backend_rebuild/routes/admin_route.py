from controllers.admin_campaign_controller import AdminCampaignController
from flask import Blueprint, jsonify, request
from flask_restful import Api
from libs.utils import auth_required, admin_required

admin_bp = Blueprint('admin', __name__)
admin_api = Api(admin_bp)

##### Campaign routes #####
@admin_bp.route("/v1/campaigns", methods=["GET"])
def get_all_campaigns():
    result = AdminCampaignController.getAllCampaigns()

    return result

@admin_bp.route("/v1/campaigns/<string:campaign_id>", methods=["GET"])
def get_single_campaign(campaign_id):
    result = AdminCampaignController.getSingleCampaign(campaign_id)

    return result

@admin_bp.route("/v1/campaigns", methods=["POST"])
def add_campaign():
    result = AdminCampaignController.addCampaign()

    return result

@admin_bp.route("/v1/campaigns/<string:campaign_id>/update", methods=["PATCH"])
def update_campaign(campaign_id):
    result = AdminCampaignController.updateCampaign(campaign_id)

    return result

@admin_bp.route("/v1/campaigns/<string:campaign_id>/cancel", methods=["PATCH"])
def cancel_campaign(campaign_id):
    result = AdminCampaignController.cancelCampaign(campaign_id)

    return result

@admin_bp.route("/v1/campaigns/<string:campaign_id>/approve", methods=["PATCH"])
def approve_campaign(campaign_id):
    result = AdminCampaignController.approveCampaign(campaign_id)

    return result

##### Artist routes #####

##### Tenant routes #####

##### User routes #####

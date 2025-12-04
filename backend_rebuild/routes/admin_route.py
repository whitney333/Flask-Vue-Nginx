from controllers.admin_campaign_controller import AdminCampaignController
from controllers.admin_tenant_controller import AdminTenantController
from controllers.admin_artist_controller import AdminArtistController
from controllers.admin_user_controller import AdminUserController
from flask import Blueprint, jsonify, request
from flask_restful import Api
from libs.utils import auth_required, admin_required

admin_bp = Blueprint('admin', __name__)
admin_api = Api(admin_bp)

##### Upload image routes #####
@admin_bp.route("/v1/artists/upload/image", methods=["POST"])
def upload_image():
    result = AdminArtistController.uploadImage()

    return result

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
@admin_bp.route("/v1/artists", methods=["GET"])
def get_all_artists():
    result = AdminArtistController.getAllArtists()

    return result

@admin_bp.route("/v1/artists/<string:artist_id>", methods=["GET"])
def get_single_artist(artist_id):
    result = AdminArtistController.getSingleArtist(artist_id)

    return result

@admin_bp.route("/v1/artists/<string:artist_id>/cancel", methods=["PATCH"])
def cancel_artist(artist_id):
    pass

@admin_bp.route("/v1/artists", methods=["POST"])
def add_artist():
    result = AdminArtistController.addArtist()

    return result

@admin_bp.route("/v1/artists/<string:artist_id>/update", methods=["PATCH"])
def update_artist(artist_id):
    result = AdminArtistController.updateArtist(artist_id)

    return result

##### Tenant routes #####
@admin_bp.route("/v1/tenants", methods=["GET"])
def get_all_tenants():
    result = AdminTenantController.getAllTenants()

    return result

@admin_bp.route("/v1/tenants/<string:tenant_id>", methods=["GET"])
def get_single_tenant(tenant_id):
    result = AdminTenantController.getSingleTenant(tenant_id)

    return result

@admin_bp.route("/v1/tenants/<string:tenant_id>/cancel", methods=["PATCH"])
def cancel_tenant(tenant_id):
    result = AdminTenantController.cancelTenant(tenant_id)

    return result

@admin_bp.route("/v1/tenants", methods=["POST"])
def add_tenant():
    result = AdminTenantController.addTenant()

    return result

@admin_bp.route("/v1/tenants/<string:tenant_id>/update", methods=["PUT"])
def update_tenant(tenant_id):
    result = AdminTenantController.updateTenant(tenant_id)

    return result

@admin_bp.route("/v1/tenants/list", methods=["GET"])
def get_tenant_dropdownlist():
    result = AdminTenantController.getTenantsList()

    return result

##### User routes #####
@admin_bp.route("/v1/users", methods=["GET"])
def get_all_users():
    result = AdminUserController.getAllUsers()

    return result

@admin_bp.route("/v1/users/<string:user_id>", methods=["GET"])
def get_single_user(user_id):
    pass

@admin_bp.route("/v1/users", methods=["POST"])
def add_user():
    pass

@admin_bp.route("/v1/users/<string:user_id>/cancel", methods=["PATCH"])
def cancel_user(user_id):
    pass
'''
updated: 2025-08-04
tenant route
- create tenant (/v1/tenant) -> POST
    - args:
        - tenant_name: string
        - tenant_description: string
        - tenant_website: string
        - tenant_email: string
    - return: tenant object
- get tenant by id (/v1/tenant/<string:tenant_id>) -> GET
    - args:
        - tenant_id: string
    - return: tenant object
- get all tenants (/v1/tenant/all) -> GET
    - args:
        - tenant_id: string
    - return: list of tenant objects
'''

from flask import Blueprint, jsonify, request
from flask_restful import Resource, reqparse, Api
from controllers.tenant_controller import TenantController

tenant_bp = Blueprint('tenant', __name__)
tenant_api = Api(tenant_bp)


@tenant_bp.route("/v1/tenant", methods=["POST"])
def create_tenant():
    """
    create new tenant
    args:
    - tenant_name: string
    - tenant_description: string
    - tenant_website: string
    - tenant_email: string
    :return: tenant object
    """
    return TenantController.create_tenant()


@tenant_bp.route("/v1/tenant/<string:tenant_id>", methods=["GET"])
def get_tenant_by_id(tenant_id):
    """
    get tenant by id
    args:
    - tenant_id: string
    :return: tenant object
    """
    return TenantController.get_tenant_by_id(tenant_id)

@tenant_bp.route("/v1/tenant/all", methods=["GET"])
def get_all_tenants():
    """
    get all tenants
    :return: list of tenant objects
    """
    return TenantController.get_all_tenants()


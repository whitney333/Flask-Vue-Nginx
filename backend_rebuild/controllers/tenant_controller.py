from models.tenant_model import Tenant
from flask import request, jsonify
from datetime import datetime
import json


class TenantController:
    @staticmethod
    def get_latest_tenant_id():
        """
        get the latest tenant id
        :return:
        """
        pipeline = [
            {"$sort": {"created_at": -1}},
            {"$limit": 1},
            {"$project": {
                "_id": 0,
                "latest_tenant_id": "$tenant_id"
            }}
        ]
        results = Tenant.objects().aggregate(pipeline)
        latest_id = list(results)

        return latest_id

    def create_tenant(self):
        """
        Create new tenant
        :return:
        """
        data = request.get_json()
        try:
            if not data.get("tenant_name") or not data.get("tenant_description"):
                return jsonify({
                    "status": "error",
                    "message": "Tenant name and description are required"
                }), 400

            if Tenant.objects(tenant_name=data.get("tenant_name")).first():
                return jsonify({
                    "status": "error",
                    "message": "Tenant name already exists"
                }), 400

            # get the latest tenant id from database
            latest_tenant_id = self.get_latest_tenant_id()
            current_tenant_id = latest_tenant_id[0] + 1
            tenant_details = {
                "tenant_id": current_tenant_id,
                "tenant_name": data.get("tenant_name"),
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
            tenant = Tenant(**tenant_details)
            tenant.save()
            print(tenant)
            return jsonify(({
                "status": "success",
                "message": "Tenant created successfully",
                "data": json.loads(tenant.to_json())
            })), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    def get_tenant_by_id(tenant_id):
        try:
            tenant = Tenant.objects(tenant_id=tenant_id).first()
            if tenant:
                return jsonify({
                    "status": "success",
                    "message": "Tenant retrieved successfully",
                    "data": json.loads(tenant.to_json())
                }), 200
            else:
                return jsonify({
                    "error": "Tenant not found"
                }), 404
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    def get_all_tenants(self):
        """
        get all tenants
        :return: list of tenant objects
        """
        try:
            tenants = Tenant.objects()
            return jsonify({
                "status": "success",
                "message": "Tenants retrieved successfully",
                "data": json.loads(tenants.to_json())
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

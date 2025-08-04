'''
updated: 2025-08-04
tenant controller
- create tenant (/v1/tenant) -> POST
    - args:
        - tenant_name: string
        - tenant_description: string
        - tenant_created_at: datetime
        - tenant_updated_at: datetime
        - tenant_website: string
        - tenant_email: string
    - return: tenant object
    - error:
        - 400: bad request
        - 404: tenant not found
        - 500: internal server error
- get tenant by id (/v1/tenant/<string:tenant_id>) -> GET
    - args:
        - tenant_id: string
    - return: tenant object
    - error:
        - 400: bad request
        - 404: tenant not found
        - 500: internal server error
- get all tenants (/v1/tenant/all) -> GET
    - return: list of tenant objects
    - error:
        - 400: bad request
        - 500: internal server error
'''
from models.tenant_model import Tenant
from flask import request, jsonify

class TenantController:
    def create_tenant():
        """
        create new tenant
        args:
        - tenant_name: string
        - tenant_description: string
        - tenant_created_at: datetime
        - tenant_updated_at: datetime
        - tenant_website: string
        - tenant_email: string
        return: tenant object
        """
        data = request.get_json()
        try:
            if not data.get("tenant_name") or not data.get("tenant_description"):
                return jsonify({"error": "Tenant name and description are required"}), 400
            
            if not data.get("tenant_website") or not data.get("tenant_email"):
                return jsonify({"error": "Tenant website and email are required"}), 400

            if Tenant.objects(tenant_name=data.get("tenant_name")).first():
                return jsonify({"error": "Tenant name already exists"}), 400
            
            
            tenant_details = {
              "tenant_name": data.get("tenant_name"),
              "tenant_created_at": datetime.now(),
              "tenant_updated_at": datetime.now(),
              "tenant_website": data.get("tenant_website"),
              "tenant_email": data.get("tenant_email"),
            }
            tenant = Tenant(**tenant_details)
            tenant.save()
            return jsonify({
                "status": "success",
                "message": "Tenant created successfully",
                "data": tenant.to_json(),
            }), 200
        except Exception as e:
            return jsonify({
                "status": "err",
                "message": str(e),
            }), 500
    
    def get_tenant_by_id(tenant_id):
        """
        get tenant by id
        args:
        - tenant_id: string
        return: tenant object
        """
        try:
            tenant = Tenant.objects(id=tenant_id).first()
            if tenant:
                return jsonify({
                    "status": "success",
                    "message": "Tenant retrieved successfully",
                    "data": tenant.to_json(),
                }), 200
            else:
                return jsonify({"error": "Tenant not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_all_tenants():
        """
        get all tenants
        return: list of tenant objects
        """
        tenants = Tenant.objects()
        return jsonify({
            "status": "success",
            "message": "Tenants retrieved successfully",
            "data": tenants.to_json(),
        }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
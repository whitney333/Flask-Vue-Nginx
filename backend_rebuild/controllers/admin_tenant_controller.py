from models.tenant_model import Tenant
from models.user_model import Users
from models.artist_model import Artists
from flask import jsonify, request
from datetime import datetime, timezone
from firebase_admin import auth
import uuid
import traceback
import re


class AdminTenantController:
    def __init__(self, admin):
        self.admin = admin

    @classmethod
    def getAllTenants(cls):
        """
                Get all tenants
                :return:
                """
        try:
            tenant_id = request.args.get("tenant_id")
            tenant_name = request.args.get("tenant_name")
            sort_field = request.args.get("sort", "tenant_id")
            order = request.args.get("order", "asc")

            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 10))

            query = {}
            if tenant_id:
                query["tenant_id"] = tenant_id
            if tenant_name:
                query["tenant_name"] = tenant_name

            tenants_query = Tenant.objects(**query)

            if order == "desc":
                tenants_query = tenants_query.order_by(f"-{sort_field}")
            else:
                tenants_query = tenants_query.order_by(sort_field)

            # pagination
            total = tenants_query.count()
            tenants = tenants_query.skip((page - 1) * limit).limit(limit)

            result = []
            for c in tenants:
                result.append({
                    "tenant_id": str(c.id) if c.id else None,
                    "tenant_number": c.tenant_id,
                    "tenant_name": str(c.tenant_name) if c.tenant_name else None,
                    "created_at": c.created_at,
                    "updated_at": c.updated_at,
                    "website": c.website,
                    "email": c.email,
                    "status": c.status,
                    "closed_at": c.closed_at
                })

            return jsonify({
                "message": "success",
                "total": total,
                "page": page,
                "limit": limit,
                "count": len(result),
                "data": result
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @classmethod
    def getSingleTenant(cls, tenant_id):
        """
        get single tenant (admin use)
        :return:
        """
        try:
            tenant = Tenant.objects(id=tenant_id).first()
            if not tenant:
                return jsonify({
                    "error": "Tenant not found"
                }), 404

            result = {
                "tenant_id": str(tenant.id) if tenant.id else None,
                "tenant_number": tenant.tenant_id,
                "tenant_name": str(tenant.tenant_name) if tenant.tenant_name else None,
                "created_at": tenant.created_at,
                "updated_at": tenant.updated_at,
                "website": tenant.website,
                "email": tenant.email,
                "status": tenant.status,
                "closed_at": tenant.closed_at
            }

            return jsonify({
                "message": "success",
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    def is_valid_email(email: str) -> bool:
        if not email:
            # allow empty
            return True
        regex = r"^[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+$"
        return re.match(regex, email) is not None

    @classmethod
    def cancelTenant(cls, tenant_id):
        try:
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                return jsonify({"error": "Missing or invalid token"}), 401

            id_token = token.split(" ")[1]
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token["uid"]

            # get user
            user = Users.objects(firebase_id=uid).first()
            if not user or not user.admin:
                return jsonify({"error": "Unauthorized"}), 403

            # get tenant
            tenant = Tenant.objects(id=tenant_id).first()

            if not tenant:
                return jsonify({"error": "Tenant not found"}), 404

            # soft delete
            tenant.status = "closed"
            tenant.closed_at = datetime.now()
            tenant.save()

            return jsonify({
                "status": "success",
                "message": f"Tenant {tenant.tenant_name} deleted."
            }), 200

        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @classmethod
    def addTenant(cls):
        """
        add a new campaign
        :return:
        """
        try:
            data = request.get_json()
            print(data)
            tenant_name = data.get("tenant_name")

            website = data.get("website")
            email = data.get("email")

            if not tenant_name:
                return jsonify({
                    "error": "tenant name and tenant number are required"
                }), 400

            # find the latest tenant number
            last_tenant = Tenant.objects().order_by("-tenant_id").first()

            if last_tenant and last_tenant.tenant_id:
                new_number = int(last_tenant.tenant_id) + 1
            else:
                new_number = 1  # first data

            new_tenant = Tenant(
                tenant_name = tenant_name,
                tenant_id = new_number,
                website = website,
                email = email
            )

            new_tenant.save()

            return jsonify({
                "message": "Tenant created successfully",
                "tenant": {
                    "tenant_id": new_tenant.tenant_id,
                    "tenant_name": new_tenant.tenant_name,
                    "created_at": new_tenant.created_at,
                    "updated_at": new_tenant.updated_at,
                    "website": new_tenant.website,
                    "email": new_tenant.email
                }
            }), 201

        except Exception as e:
            print(traceback.format_exc())
            return jsonify({
                "error": str(e)
            }), 500

    @classmethod
    def updateTenant(cls, tenant_id):
        """
        modify tenant details: name, website, email
        :return:
        """
        try:
            data = request.get_json()

            tenant = Tenant.objects(id=tenant_id).first()
            if not tenant:
                return jsonify({"error": "Tenant not found"}), 404

            tenant_name = data.get("tenant_name")
            website = data.get("website")
            email = data.get("email")
            status = data.get("status")

            # tenant_name check
            if not tenant_name:
                return jsonify({"error": "tenant_name is required"}), 400
            # email check
            if email and not cls.is_valid_email(email):
                return jsonify({"error": "Invalid email format"}), 400
            # double check if email has been used
            if email and Tenant.objects(email=email, id__ne=tenant.id).first():
                return jsonify({"error": "Email already used by another tenant"}), 409
            if status in ["active", "suspended", "closed"]:
                tenant.status = status
                if status == "closed":
                    tenant.closed_at = datetime.now()
                else:
                    tenant.closed_at = None

            # update value
            tenant.tenant_name = tenant_name
            tenant.website = website
            tenant.email = email
            tenant.updated_at = datetime.now()
            tenant.save()

            return jsonify({
                "message": "Tenant updated successfully",
                "tenant": {
                    "_id": str(tenant.id),
                    "tenant_name": tenant.tenant_name,
                    "website": tenant.website,
                    "email": tenant.email,
                    "status": tenant.status,
                    "created_at": tenant.created_at,
                    "updated_at": tenant.updated_at,
                    "closed_at": tenant.closed_at
                }
            }), 200

        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

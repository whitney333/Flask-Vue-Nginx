from models.campaign_model import Campaign, CampaignTotalRegion, CampaignTotalCountry, CampaignTotalPlatform, CampaignPost
from models.user_model import Users
from models.artist_model import Artists
from flask import jsonify, request
from datetime import datetime, timezone
from firebase_admin import auth
import uuid


class AdminCampaignController:
    def __init__(self, admin):
        self.admin = admin

    @classmethod
    def getAllCampaigns(cls):
        """
        Get all campaigns
        :return:
        """
        try:
            status = request.args.get("status")
            user_id = request.args.get("user_id")
            artist_id = request.args.get("artist_id")
            sort_field = request.args.get("sort", "created_at")
            order = request.args.get("order", "desc")

            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 10))
            from_date = request.args.get("from")
            to_date = request.args.get("to")

            allowed_sort_fields = ["created_at", "approved_at", "status"]
            if sort_field not in allowed_sort_fields:
                return jsonify({"error": f"Invalid sort field: {sort_field}"}), 400

            query = {}
            if status:
                query["status"] = status
            if user_id:
                query["user_id"] = user_id
            if artist_id:
                query["artist_id"] = artist_id

            if from_date or to_date:
                date_filter = {}
                if from_date:
                    date_filter["$gte"] = datetime.fromisoformat(from_date)
                if to_date:
                    date_filter["$lte"] = datetime.fromisoformat(to_date)
                query["created_at"] = date_filter

            campaigns_query = Campaign.objects(**query)

            if order == "desc":
                campaigns_query = campaigns_query.order_by(f"-{sort_field}")
            else:
                campaigns_query = campaigns_query.order_by(sort_field)

            # pagination
            total = campaigns_query.count()
            campaigns = campaigns_query.skip((page - 1) * limit).limit(limit)

            result = []
            for c in campaigns:
                result.append({
                    "campaign_id": str(c.campaign_id),
                    "status": c.status,
                    "user_id": str(c.user_id.id) if c.user_id else None,
                    "user_name" : str(c.user_id.name) if c.user_id else None,
                    "user_email": str(c.user_id.email) if c.user_id else None,
                    "artist_id": str(c.artist_id.id) if c.artist_id else None,
                    "approved_at": c.approved_at,
                    "created_at": c.created_at,
                    "cancelled_at": c.cancelled_at,
                    "cancelled_by": c.cancelled_by
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
    def getSingleCampaign(cls, campaign_id):
        """
        get single campaign (admin use)
        :return:
        """
        try:
            campaign = Campaign.objects(campaign_id=campaign_id).first()
            if not campaign:
                return jsonify({
                    "error": "Campaign not found"
                }), 404

            result = {
                "campaign_id": str(campaign.campaign_id),
                "user_id": str(campaign.user_id.id) if campaign.user_id else None,
                "created_at": campaign.created_at,
                "status": campaign.status,
                "artist_id": str(campaign.artist_id.id) if campaign.artist_id else None,
                "artist_en_name": campaign.artist_en_name if campaign.artist_id else None,
                "artist_kr_name": campaign.artist_kr_name if campaign.artist_id else None,
                "budget": campaign.budget,
                "user_target_region": campaign.region,
                "user_target_platform": campaign.platform,
                "user_post_info": campaign.info,
                "post": [r.to_mongo() for r in campaign.post] if campaign.post else [],
                "actual_cost": campaign.total_cost,
                "actual_reach": campaign.total_reach,
                "actual_region": [r.to_mongo() for r in campaign.total_region] if campaign.total_region else [],
                "actual_country": [r.to_mongo() for r in campaign.total_country] if campaign.total_country else [],
                "actual_platform": [r.to_mongo() for r in campaign.total_platform] if campaign.total_platform else [],
            }

            return jsonify({
                "message": "success",
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @classmethod
    def addCampaign(cls):
        """
        add a new campaign
        :return:
        """
        try:
            data = request.get_json()

            # every campaign should under user account
            # get user ObjectId
            user_objId = Users.objects(firebase_id=data.get("firebase_id")).first()
            if not user_objId:
                return jsonify({"error": "User not found"}), 404

            # get artist ObjectId
            artist_objId = Artists.objects(artist_id=data.get("artist")).first()
            if not artist_objId:
                return jsonify({"error": "Artist not found"}), 404
            # print(artist_objId.id)
            # generate campaign id
            random_uuid = str(uuid.uuid4())
            campaign_id = random_uuid[:8]

            # create campaign
            campaign = Campaign(
                campaign_id=campaign_id,
                user_id=user_objId,
                created_at=datetime.now(),
                artist_id=artist_objId,
                artist_en_name=data.get("artist_en_name"),
                artist_kr_name=data.get("artist_kr_name"),
                platform=data.get("platform"),
                region=data.get("region"),
                budget=data.get("budget"),
                status=data.get("status"),
                approved_at=None,
                cancelled_at=None,
                cancelled_by=None,
                info=data.get("info"),
                post=[],
                total_cost=None,
                total_reach=None,
                total_platform=[],
                total_country=[]
            )
            campaign.save()

            return jsonify({
                "message": "Campaign created successfully",
                "data": str(campaign.campaign_id),
                "timestamp": campaign.created_at
            }), 201

        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @classmethod
    def convert_list_to_embedded(cls, front_field, items):
        if front_field == "actual_region":
            return [CampaignTotalRegion(name=i["name"], count=i["count"]) for i in items]

        if front_field == "actual_country":
            return [CampaignTotalCountry(name=i["name"], count=i["count"], region=i.get("region")) for i in items]

        if front_field == "actual_platform":
            return [CampaignTotalPlatform(name=i["name"], count=i["count"]) for i in items]

        return items  # fallback: return raw items

    @staticmethod
    def clean_post_data(post):
        cleaned = post.copy()

        # convert to int
        numeric_fields = ["reach", "reaction", "latest_view", "one_hour_view", "twentyfour_hour_view", "hashtag_reach",
                          "cost"]
        for field in numeric_fields:
            if field in cleaned:
                try:
                    cleaned[field] = int(str(cleaned[field]).replace("$", "").replace(",", ""))
                except:
                    cleaned[field] = 0

        # used_hashtag: list
        if "used_hashtag" in cleaned and not isinstance(cleaned["used_hashtag"], list):
            cleaned["used_hashtag"] = []

        return cleaned

    @classmethod
    def updateCampaign(cls, campaign_id):
        """
        modify campaign details
        :return:
        """
        try:
            data = request.json
            print(data)
            campaign = Campaign.objects(campaign_id=campaign_id).first()
            if not campaign:
                return jsonify({"error": "Campaign not found"}), 404

            field_mapping = {
                # map field name to db field name
                "user_target_region": "region",
                "budget": "budget",
                "user_target_platform": "platform",
                "user_post_info": "info",
                # performance fields
                "actual_region": "total_region",
                "actual_country": "total_country",
                "actual_platform": "total_platform",
                # post fields
                "post": "post"
            }

            for front_field, db_field in field_mapping.items():

                if front_field not in data:
                    continue

                new_value = data[front_field]

                # --- post update ---
                if front_field == "post":
                    if isinstance(new_value, list):
                        # clear post
                        campaign.post.clear()
                        for p in new_value:
                            campaign.post.append(CampaignPost(**cls.clean_post_data(p)))
                    elif isinstance(new_value, dict) and "url" in new_value:
                        # identify by url
                        target_url = new_value["url"]
                        updated = False
                        for existing in campaign.post:
                            if existing.url == target_url:
                                for key, val in new_value.items():
                                    if key != "url" and hasattr(existing, key):
                                        setattr(existing, key, val)
                                updated = True
                                break
                        if not updated:
                            return jsonify({
                                "error": f"Post with url {target_url} not found"
                            }), 404
                    continue

                # --- other fields except post ---
                new_value = cls.convert_list_to_embedded(front_field, new_value)
                setattr(campaign, db_field, new_value)

            campaign.save()

            return jsonify({
                "message": "Campaign updated successfully"
            }), 200

        except Exception as e:
            return jsonify({
                "err": str(e)
            }), 500

    @classmethod
    def cancelCampaign(cls, campaign_id):
        """
        cancel a campaign (admin use)
        :return:
        """
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

            campaign = Campaign.objects(campaign_id=campaign_id).first()
            if not campaign:
                return jsonify({
                    "error": "Campaign not found"
                }), 404

            # if campaign has been cancelled
            if campaign.status == "cancelled":
                return jsonify({
                    "message": "Campaign already cancelled"
                }), 200

            # if not, change to cancelled status
            campaign.status = "cancelled"
            campaign.cancelled_at = datetime.now(timezone.utc)
            campaign.cancelled_by = str(user.id)
            campaign.save()

            return jsonify({
                "message": f"Campaign {campaign_id} cancelled successfully",
                "cancelled_at": campaign.cancelled_at,
                "cancelled_by": user.name
            }), 200

        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @classmethod
    def approveCampaign(cls, campaign_id):
        """
        approve campaign status when the package is confirmed
        :return:
        """
        campaign = Campaign.objects(campaign_id=campaign_id).first()
        if not campaign:
            return jsonify({"error": "Campaign not found"}), 404

        if campaign.status == "approved":
            return jsonify({"message": "Already approved"}), 200

        campaign.status = "approved"
        campaign.approved_at = datetime.now(timezone.utc)
        campaign.save()

        return jsonify({
            "message": f"Campaign {campaign_id} approved successfully",
            "approved_at": campaign.approved_at
        }), 200


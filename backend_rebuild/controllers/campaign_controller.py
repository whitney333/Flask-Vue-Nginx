from models.campaign_model import Campaign
from models.user_model import Users
from models.artist_model import Artists
from flask import request, jsonify
from firebase_admin import auth
import datetime
import uuid


class CampaignController:

    @classmethod
    def create_campaign(cls):
        """
        create new campaign
        :return:
        """
        try:
            # get token from header
            id_token = request.headers.get("Authorization", "").replace("Bearer ", "")

            if not id_token:
                return jsonify({"error": "Missing token"}), 401

            # verify token
            # decoded_token = auth.verify_id_token(id_token)
            # uid = decoded_token["uid"]

            # get data
            data = request.get_json()
            print("Received data: ", data)

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
            campaign_id = "CP-" + random_uuid[:8]

            # store data
            new_campaign = Campaign(
                campaign_id = campaign_id,
                user_id = user_objId,
                created_at = datetime.datetime.now(),
                artist_id = artist_objId,
                artist_en_name = data.get("artist_en_name"),
                artist_kr_name = data.get("artist_kr_name"),
                platform = data.get("platform"),
                region = data.get("region"),
                budget = data.get("budget"),
                status = data.get("status"),
                post = [],
                total_cost = None,
                total_reach = None,
                total_platform = [],
                total_country = []
            )

            new_campaign.save()


            return jsonify({
                "status": "success",
                "message": "Campaign created successfully",
            }), 201

        except Exception as e:
            return jsonify({
                "err": str(e)
            }), 500

    @classmethod
    def cancel_campaign(cls, campaign_id):
        """
        soft delete campaign
        :return:
        """
        try:
            # get token from header
            id_token = request.headers.get("Authorization", "").replace("Bearer ", "")

            if not id_token:
                return jsonify({"error": "Missing token"}), 401

            try:
                # verify token, get user firebase_id
                decoded_token = auth.verify_id_token(id_token)
                uid = decoded_token["uid"]
            except Exception as e:
                return jsonify({"error": f"Invalid token: {str(e)}"}), 401

            data = request.get_json()
            print("data: ", data)
            status = data.get("status")

            # find the campaign
            campaign = Campaign.objects(campaign_id=campaign_id).first()

            if not campaign:
                return jsonify({"error": "Campaign not found"}), 404

            if status:
                campaign.update(status=status)

            return jsonify({
                "status": "success",
                "message": "Campaign updated successfully"
            }), 200

        except Exception as e:
            return jsonify({
                "err": str(e)
            }), 500

    @classmethod
    def update_campaign(cls):
        """
        update campaign information
        :return:
        """
        pass

    @classmethod
    def get_all_campaign_by_user_id(cls):
        try:
            # get token from header
            id_token = request.headers.get("Authorization", "").replace("Bearer ", "")

            if not id_token:
                return jsonify({"error": "Missing token"}), 401

            try:
                # verify token, get user firebase_id
                decoded_token = auth.verify_id_token(id_token)
                uid = decoded_token["uid"]
            except Exception as e:
                return jsonify({"error": f"Invalid token: {str(e)}"}), 401

            # get user ObjectId by firebase id
            user_objId = Users.objects(firebase_id=uid).first()
            if not user_objId:
                return jsonify({"error": "User not found"}), 404


            campaigns = Campaign.objects(user_id=user_objId).only(
                # keep needed fields
                "campaign_id", "created_at", "artist_en_name", "artist_kr_name",
                "platform", "region", "budget", "status"
            ).order_by("-created_at")
            campaign = [
                {
                    "campaign_id": str(c.campaign_id),
                    "created_at": c.created_at,
                    "artist_en_name": c.artist_en_name,
                    "artist_kr_name": c.artist_kr_name,
                    "platform": c.platform,
                    "region": c.region,
                    "budget": c.budget,
                    "status": c.status} for c in campaigns
            ]

            return jsonify({
                "status": "success",
                "data": campaign
            }), 200

        except Exception as e:
            return jsonify({
                "err": str(e)
            }), 500

    @classmethod
    def get_per_campaign_by_campaign_id(cls):
        try:
            # get token from header
            id_token = request.headers.get("Authorization", "").replace("Bearer ", "")

            if not id_token:
                return jsonify({"error": "Missing token"}), 401

            try:
                # verify token, get user firebase_id
                decoded_token = auth.verify_id_token(id_token)
                uid = decoded_token["uid"]
            except Exception as e:
                return jsonify({"error": f"Invalid token: {str(e)}"}), 401

        except Exception as e:
            return jsonify({
                "err": str(e)
            }), 500


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

            # store data
            new_campaign = Campaign(
                campaign_id = str(uuid.uuid4()),
                user_id = user_objId,
                created_at = datetime.datetime.now(),
                artist = artist_objId,
                platform = data.get("platform"),
                region = data.get("region"),
                budget = data.get("budget"),
                post = []
            )

            new_campaign.save()


            return jsonify({
                "status": "success",
                "data": "1"
            }), 201

        except Exception as e:
            return jsonify({
                "err": str(e)
            }), 500

    @classmethod
    def delete_campaign(cls):
        """
        delete campaign
        :return:
        """
        pass

    @classmethod
    def update_campaign(cls):
        """
        update campaign information
        :return:
        """
        pass

    @classmethod
    def get_all_campaign(cls):
        try:
            # get token from header
            id_token = request.headers.get("Authorization", "").replace("Bearer ", "")

            if not id_token:
                return jsonify({"error": "Missing token"}), 401



        except Exception as e:
            return jsonify({
                "err": str(e)
            }), 500

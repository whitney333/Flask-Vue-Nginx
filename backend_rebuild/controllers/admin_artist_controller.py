from models.tenant_model import Tenant
from models.user_model import Users
from models.artist_model import Artists
from flask import jsonify, request
from datetime import datetime, timezone
from firebase_admin import auth
from mongoengine.errors import ValidationError
from bson import ObjectId
import re
import os
import uuid
import boto3
from dotenv import load_dotenv
import traceback


class AdminArtistController:
    def __init__(self, admin):
        self.admin = admin

    @classmethod
    def getAllArtists(cls):
        """
        Get all artist
        :return:
        """
        try:
            artist_id = request.args.get("artist_id")
            english_name = request.args.get("name")
            order = request.args.get("order", "asc")
            type = request.args.get("type")

            pronouns = request.args.get("pronouns")
            debut_year = request.args.get("debut_year")

            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 10))

            sort_order = -1 if order == "desc" else 1
            pipeline = []

            # Query
            query = {}
            if artist_id:
                query["artist_id"] = artist_id

            if type:
                query["type"] = {"$in": type.split(",")}

            if pronouns:
                query["pronouns"] = pronouns

            if debut_year:
                try:
                    year = int(debut_year)
                    query["debut_year"] = year
                except ValueError:
                    pass

            if english_name:
                query["english_name"] = {"$regex": english_name, "$options": "i"}

            if query:
                pipeline.append({"$match": query})

            # pipeline with sorting
            pipeline.append({
                "$addFields": {
                    "artist_id": {"$toInt": "$artist_id"}
                }
            })
            pipeline.append({"$sort": {"artist_id": sort_order}})
            pipeline.append({"$skip": (page - 1) * limit})
            pipeline.append({"$limit": limit})
            pipeline.append({
                "$project": {
                    "_id": 1,
                    "artist_id": 1,
                    "english_name": 1,
                    "korean_name": 1,
                    "debut_year": 1,
                    "birth": 1,
                    "type": 1,
                    "pronouns": 1,
                    "image_url": 1,
                    "tenant_id": {"$toString": "$tenant_id"}
                }
            })
            artists = list(Artists.objects.aggregate(pipeline))
            total = Artists.objects(**query).count()


            result = []
            for a in artists:
                # get tenant name
                tenant = Tenant.objects(id=a.get("tenant_id")).first()

                result.append({
                    "id": str(a["_id"]),
                    "artist_id": a.get("artist_id"),
                    "artist_en_name": a.get("english_name"),
                    "artist_kr_name": a.get("korean_name"),
                    "debut": a.get("debut_year"),
                    "birth": a.get("birth"),
                    "belong_tenant": tenant.tenant_name if tenant else None,
                    "pronouns": a.get("pronouns"),
                    "type": a.get("type"),
                    "image": a.get("image_url")
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
            return jsonify({
                "error": str(e)
            }), 500

    @classmethod
    def getSingleArtist(cls, artist_id):
        """
        get single artist (admin use)
        :return:
        """
        try:
            artist = Artists.objects(id=artist_id).first()
            if not artist:
                return jsonify({
                    "error": "Artist not found"
                }), 404

            result = {
                # basic info
                "id": str(artist.id) if artist.id else None,
                "tenant_id": str(artist.tenant_id.id) if artist.tenant_id else None,
                "tenant_name": str(artist.tenant_id.tenant_name) if artist.tenant_id else None,
                "artist_id": str(artist.artist_id) if artist.artist_id else None,
                "artist_en_name": str(artist.english_name) if artist.english_name else None,
                "artist_kr_name": str(artist.korean_name) if artist.korean_name else None,
                "debut": artist.debut_year,
                "birth": artist.birth,
                "nation": artist.nation,
                "pronouns": artist.pronouns,
                "type": artist.type,
                "fandom": artist.fandom,
                "image": artist.image_url,
                # TODO BELONG GROUP > REFERENCE FIELD
                # sns
                "instagram_id": artist.instagram_id,
                "instagram_user": artist.instagram_user,
                "threads": artist.threads,
                "tiktok_id": artist.tiktok_id,
                "bilibili_id": artist.bilibili_id,
                "weibo_id": artist.weibo_id,
                # music
                "spotify_id": artist.spotify_id,
                "youtube_id": artist.youtube_id,
                "melon_id": artist.melon_id,
                "genie_id": artist.genie_id,
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
    def addArtist(cls):
        """

        :return:
        """
        try:
            data = request.get_json()

            # required data fields
            required_fields = {
                "english_name": "english_name is required",
                "korean_name": "korean_name is required",
                "tenant_id": "tenant_id is required",
                "type": "type is required",
                "pronouns": "pronouns is required"
            }

            for field, msg in required_fields.items():
                if not data.get(field):
                    return jsonify({"error": msg}), 400

            english_name = data.get("english_name")
            korean_name = data.get("korean_name")
            debut_year = data.get("debut_year")
            type = data.get("type")
            birth = data.get("birth")
            fandom = data.get("fandom")
            tenant_id = data.get("tenant_id")
            nation = data.get("nation")
            pronouns = data.get("pronouns")
            image_url = data.get("image_url")
            instagram_id = data.get("instagram_id")
            instagram_user = data.get("instagram_user")
            threads = data.get("threads")
            tiktok_id = data.get("tiktok_id")
            bilibili_id = data.get("bilibili_id")
            weibo_id = data.get("weibo_id")
            youtube_id = data.get("youtube_id")
            spotify_id = data.get("spotify_id")
            apple_id = data.get("apple_id")
            melon_id = data.get("melon_id")
            genie_id = data.get("genie_id")

            # ==== Validate type ====
            if not isinstance(type, list):
                return jsonify({"error": "type must be an array"}), 400

            if len(type) == 0:
                return jsonify({"error": "type cannot be empty"}), 400
            # Debut year type
            if debut_year:
                try:
                    debut_year = int(debut_year)
                except:
                    return jsonify({"error": "debut_year must be integer"}), 400
            else:
                debut_year = None
            # ==== Validate birth date ====
            birth_date = None
            if birth:
                try:
                    birth_date = datetime.fromisoformat(birth).date()
                except ValueError:
                    return jsonify({
                        "error": "Invalid birth date format. Use YYYY-MM-DD"
                    }), 400

            # ==== Validate tenant exists ====
            tenant = Tenant.objects(id=tenant_id).first()
            if not tenant:
                return jsonify({"error": "Invalid tenant_id"}), 400

            # ==== Duplicate artist check ====
            existed = Artists.objects(
                english_name__iexact=english_name
            ).first()

            if existed:
                return jsonify({
                    "error": "Artist with this English name already exists"
                }), 409

            check_last_artist_pipeline = [
                {"$project": {
                    "artist_id": {"$toInt": "$artist_id"}
                }},
                {"$sort": {"artist_id": -1}},
                {"$limit": 1}
            ]
            cursor  = Artists.objects().aggregate(check_last_artist_pipeline)
            last_artist = next(cursor, None)

            if last_artist and "artist_id" in last_artist:
                next_id = str(last_artist["artist_id"] + 1)
            else:
                next_id = "1"

            # create artist
            artist = Artists(
                artist_id = next_id,
                english_name = english_name,
                korean_name = korean_name,
                debut_year = debut_year,
                type = type,
                birth = birth_date,
                fandom = fandom,
                tenant_id = tenant,
                nation = nation,
                pronouns = pronouns,
                image_url = image_url,
                instagram_id = instagram_id,
                instagram_user= instagram_user,
                threads = threads,
                tiktok_id = tiktok_id,
                bilibili_id = bilibili_id,
                weibo_id = weibo_id,
                youtube_id = youtube_id,
                spotify_id = spotify_id,
                apple_id = apple_id,
                melon_id = melon_id,
                genie_id = genie_id
            )
            artist.save()

            return jsonify({
                "status": "success",
                "message": "Artist added successfully",
                "id": str(artist.id),
                "artist_id": artist.artist_id,
                "english_name": artist.english_name,
                "korean_name": artist.korean_name,
                "image_url": artist.image_url,
                "tenant_name": tenant.tenant_name
            }), 201

        except Exception as e:
            print(traceback.format_exc())
            return jsonify({
                "error": str(e)
            }), 500

    @staticmethod
    def normalize_string(v):
        if v in ("", None, "null"):
            return None
        return str(v)

    @classmethod
    def updateArtist(cls, artist_id):
        """
        modify artist details
        :return:
        """
        try:
            data = request.get_json()
            print(data)

            artist = Artists.objects(id=artist_id).first()
            if not artist:
                return jsonify({"error": "Artist not found"}), 404

            # TODO MISS BELONG_GROUPS, COMPANY, IMAGE
            basic_fields = [
                'tenant_id', 'tenant_name', 'artist_id',
                'english_name', 'korean_name', 'pronouns',
                'type', 'debut_year', 'birth', 'fandom',
                'image_url'
            ]

            sns_fields = [
                'instagram_id', 'instagram_user', 'threads',
                'youtube_id', 'tiktok_id',
                'bilibili_id', 'weibo_id',
                'spotify_id', 'melon_id', 'genie_id'
            ]


            # update fields
            for key, value in data.items():
                if key in sns_fields:
                    # threads
                    if key == "threads":
                        if value in ("", None):
                            setattr(artist, key, None)
                        else:
                            setattr(artist, key, bool(value))
                    else:
                        setattr(artist, key, cls.normalize_string(value))
                    continue

                elif key in basic_fields:
                    # check artist_id
                    if key == "artist_id" and value:
                        artist.artist_id = cls.normalize_string(value)
                        continue

                    if key == 'tenant_id' and value:
                        tenant = Tenant.objects(id=value).first()
                        if not tenant:
                            return jsonify({"error": "Tenant not found"}), 400

                        artist.tenant_id = tenant
                        continue
                    # convert to datetime
                    if key == 'birth' and value:
                        if value in ("", None):
                            artist.birth = None
                        else:
                            try:
                                if isinstance(value, str):
                                    artist.birth = datetime.fromisoformat(value)
                                else:
                                    artist.birth = value
                            except ValueError:
                                return jsonify({"error": "Invalid birth date format"}), 400
                        continue
                    # debut_year
                    if key == "debut_year":
                        if value in ("", None):
                            artist.debut_year = None
                        else:
                            try:
                                artist.debut_year = int(value)
                            except ValueError:
                                return jsonify({"error": "debut_year must be an integer"}), 400
                        continue

                    # type / artist_type
                    if key in ("type", "artist_type"):
                        if isinstance(value, list):
                            artist.type = value
                        elif value in ("", None):
                            artist.type = []
                        else:
                            return jsonify({"error": "type must be a list"}), 400
                        continue

                    if key == 'image_url':
                        setattr(artist, key, cls.normalize_string(value))

                    # korean_name / english_name / pronouns / fandom / etc.
                    setattr(artist, key, cls.normalize_string(value))
                    continue
                else:
                    # update other fields
                    setattr(artist, key, value)

            try:
                artist.save()
            except ValidationError as ve:
                return jsonify({"error": f"Validation failed: {ve}"}), 400

            return jsonify({
                "message": "Artist updated successfully",
                "id": str(artist.id)
            }), 200

        except Exception as e:
                print(traceback.format_exc())
                return jsonify({
                    "error": str(e)
                }), 500

    @classmethod
    def cancelArtist(cls, artist_id):
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

            # get artist
            artist = Artists.objects(id=artist_id).first()

            if not artist:
                return jsonify({"error": "Artist not found"}), 404


        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @staticmethod
    def slugify_name(name: str):
        # lower
        name = name.lower()
        # space => -
        name = name.replace(" ", "-")
        # keep english, number, -
        return re.sub(r'[^a-z0-9\-]', '', name)

    @classmethod
    def uploadImage(cls):
        file = request.files.get("file")
        artist_id = request.form.get("artist_id", "")
        artist_name = request.form.get("artist_name", "")

        if not file:
            return jsonify({
                "error": "No file provided"
            }), 400

        ext = file.filename.split('.')[-1].lower()
        if ext not in {"jpg", "jpeg", "png", "webp"}:
            return jsonify({
                "error": "Invalid file type"
            }), 400

        clean_name = cls.slugify_name(artist_name)
        filename = f"{artist_id}-{clean_name}.{ext}"

        try:
            environment = os.getenv("FLASK_ENV", "development")  # default to 'dev'
            env_file = f".env.{environment}"
            if os.path.exists(env_file):
                load_dotenv(dotenv_path=env_file)

            # client init
            client = boto3.client(
                "s3",
                region_name=os.getenv(key="AWS_S3_REGION"),
                aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
            )

            # file: name of file on local
            # bucket: bucket name
            # filename: name of file on s3 bucket
            # args: custom arguments
            bucket = os.getenv("AWS_S3_BUCKET")
            region = os.getenv("AWS_S3_REGION")
            response = client.upload_fileobj(
                file,
                bucket,
                f"artist-profile/{filename}",
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )
            url = f"https://{bucket}.s3.{region}.amazonaws.com/artist-profile/{filename}"
            print(url)
            return jsonify({"url": url}), 200

        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @classmethod
    def getArtistsList(cls):
        """
            Get all artists for dropdown list
            :return:
        """
        try:
            artists = Artists.objects.only("id", "english_name")

            result = [
                {
                    "id": str(c.id),
                    "artist": c.english_name
                }
                for c in artists
            ]

            return jsonify({
                "message": "success",
                "data": result
            }), 200

        except Exception as e:
            return jsonify({
                "err": str(e)
            }), 500

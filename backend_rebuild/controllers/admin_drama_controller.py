from models.drama_model import Drama
from bson import ObjectId
from models.tenant_model import Tenant
from flask import jsonify, request


class AdminDramaController:
    def __init__(self, admin):
        self.admin = admin

    @classmethod
    def get_all_dramas(cls):
        """
        Get all dramas from the database
        :return:
        """
        try:
            drama_id = request.args.get("drama_id")
            name = request.args.get("name")
            order = request.args.get("order", "asc")
            type = request.args.get("type")

            broadcast_year = request.args.get("broadcast_year")

            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 10))

            sort_order = -1 if order == "desc" else 1
            pipeline = []

            # Query
            query = {}
            if drama_id:
                query["drama_id"] = drama_id

            if type:
                query["type"] = {"$in": type.split(",")}

            if broadcast_year:
                try:
                    year = int(broadcast_year)
                    query["broadcast_year"] = year
                except ValueError:
                    pass

            if name:
                query["$or"] = [
                    {"name": {"$regex": name, "$options": "i"}},
                    {"name_in_korean": {"$regex": name, "$options": "i"}}
                ]

            if query:
                pipeline.append({"$match": query})

            # pipeline with sorting
            pipeline.append({"$sort": {"drama_sequence": sort_order}})
            pipeline.append({"$skip": (page - 1) * limit})
            pipeline.append({"$limit": limit})
            
            dramas = list(Drama.objects.aggregate(pipeline))
            total = Drama.objects(**query).count()
            
            import math
            last_page = math.ceil(total / limit) if total > 0 else 1

            result = []
            for d in dramas:
                result.append({
                    "id": str(d["_id"]),
                    "drama_id": d.get("drama_id"),
                    "name": d.get("name"),
                    "name_in_korean": d.get("name_in_korean"),
                    "broadcast_year": d.get("broadcast_year"),
                    "onair_date": d.get("onair_date").strftime("%Y-%m-%d") if d.get("onair_date") else None,
                    "country": d.get("country"),
                    "episode": d.get("episode"),
                    "type": d.get("type"),
                    "genre": d.get("genre"),
                    "thumbnail": d.get("thumbnail")
                })

            return jsonify({
                "message": "success",
                "total": total,
                "page": page,
                "first_page": 1,
                "last_page": last_page,
                "limit": limit,
                "count": len(result),
                "data": result
            }), 200
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @classmethod
    def get_drama_by_id(cls, drama_id):
        try:
            drama = Drama.objects(id=drama_id).first()
            if not drama:
                return jsonify({"message": "Drama not found"}), 404
            
            # return formatted data
            data = {
                "id": str(drama.id),
                "drama_id": drama.drama_id,
                "name": drama.name,
                "name_in_korean": drama.name_in_korean,
                "onair_date": drama.onair_date.strftime("%Y-%m-%d") if drama.onair_date else None,
                "broadcast_day": drama.broadcast_day,
                "broadcast_time": drama.broadcast_time.strftime("%H:%M") if drama.broadcast_time else None,
                "broadcast_year": drama.broadcast_year,
                "country": drama.country,
                "episode": drama.episode,
                "special_episode": drama.special_episode,
                "finale": drama.finale.strftime("%Y-%m-%d") if drama.finale else None,
                "genre": drama.genre,
                "type": drama.type,
                "language": drama.language,
                "premiere_channel": drama.premiere_channel,
                "streaming": drama.streaming,
                "director": drama.director,
                "production": drama.production,
                "screenwriter": drama.screenwriter,
                "starring": [
                    str(s.id) if hasattr(s, "id") else str(s)
                    for s in (drama.starring or [])
                ],
                "thumbnail": drama.thumbnail_url
            }

            return jsonify({"message": "success", "data": data}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @classmethod
    def add_drama(cls):
        try:
            data = request.get_json()
            print(data)
            
            year = data.get("broadcast_year")
            if not year:
                return jsonify({"message": "broadcast_year is required"}), 400

            name = data.get("name")
            if name and Drama.objects(name=name, broadcast_year=year).first():
                return jsonify({"message": "Drama already exists"}), 409

            # Generate drama_id and drama_sequence automatically
            # Logic: D + 3-digit sequence (e.g. D001)
            
            last_drama = Drama.objects.order_by("-drama_sequence").first()
            sequence = 1
            if last_drama:
                sequence = last_drama.drama_sequence + 1
            
            drama_id = f"D{str(sequence).zfill(3)}"
            
            # Create drama
            broadcast_time = data.get("broadcast_time")
            if broadcast_time and isinstance(broadcast_time, str):
                if len(broadcast_time) <= 5: # HH:mm
                    broadcast_time = f"1970-01-01 {broadcast_time}:00"
                elif len(broadcast_time) <= 8: # HH:mm:ss
                    broadcast_time = f"1970-01-01 {broadcast_time}"
            
            raw_starring = data.get("starring")
            starring_list = []
            if isinstance(raw_starring, list):
                for item in raw_starring:
                    if isinstance(item, dict):
                        value = item.get("mid") or item.get("artist_id") or item.get("id")
                    else:
                        value = item
                    if not value:
                        continue
                    try:
                        starring_list.append(ObjectId(str(value)))
                    except Exception:
                        continue

            drama = Drama(
                drama_id=drama_id,
                drama_sequence=sequence,
                name=data.get("name"),
                name_in_korean=data.get("name_in_korean"),
                onair_date=data.get("onair_date"),
                broadcast_day=data.get("broadcast_day") if isinstance(data.get("broadcast_day"), list)
                else (data.get("broadcast_day").split(",") if data.get("broadcast_day") and isinstance(data.get("broadcast_day"), str) else []),
                broadcast_time=broadcast_time,
                broadcast_year=year,
                country=data.get("country"),
                episode=int(data.get("episode")) if data.get("episode") else 0,
                special_episode=int(data.get("special_episode")) if data.get("special_episode") else 0,
                finale=data.get("finale"),
                genre=data.get("genre") if isinstance(data.get("genre"), list) else [],
                type=data.get("type"),
                language=data.get("language"),
                premiere_channel=data.get("premiere_channel") if isinstance(data.get("premiere_channel"), list)
                else (data.get("premiere_channel").split(",") if data.get("premiere_channel") and isinstance(data.get("premiere_channel"), str) else []),
                streaming=data.get("streaming") if isinstance(data.get("streaming"), list)
                else (data.get("streaming").split(",") if data.get("streaming") and isinstance(data.get("streaming"), str) else []),
                director=data.get("director").split(",") if data.get("director") and isinstance(data.get("director"), str) else [],
                production=data.get("production").split(",") if data.get("production") and isinstance(data.get("production"), str) else [],
                screenwriter=data.get("screenwriter").split(",") if data.get("screenwriter") and isinstance(data.get("screenwriter"), str) else [],
                starring=starring_list,
                thumbnail_url=data.get("thumbnail")
            )
            
            drama.save()
            return jsonify({
                "message": "success",
                "drama_id": drama_id,
                "drama_seq": sequence
            }), 201
        except Exception as e:
            return jsonify({
                "error": str(e)
            }), 500

    @classmethod
    def update_drama(cls, drama_id):
        try:
            data = request.json
            drama = Drama.objects(id=drama_id).first()
            if not drama:
                return jsonify({"message": "Drama not found"}), 404
            
            # Update fields
            # Handle list fields (split if string)
            list_fields = ["broadcast_day", "premiere_channel", "streaming", "director", "production", "screenwriter"]
            
            for key, value in data.items():
                if key in ["id", "_id", "drama_id", "drama_sequence"]:
                    continue
                    
                if hasattr(drama, key):
                    if key == "starring":
                        normalized = []
                        if isinstance(value, list):
                            for item in value:
                                if isinstance(item, dict):
                                    raw = item.get("mid") or item.get("artist_id") or item.get("id")
                                else:
                                    raw = item
                                if not raw:
                                    continue
                                try:
                                    normalized.append(ObjectId(str(raw)))
                                except Exception:
                                    continue
                        setattr(drama, key, normalized)
                        continue
                    if key in list_fields:
                        if isinstance(value, list):
                            setattr(drama, key, value)
                        elif isinstance(value, str):
                            setattr(drama, key, value.split(","))
                        else:
                            setattr(drama, key, [])
                    elif key == "broadcast_time" and value and isinstance(value, str):
                        if len(value) <= 5: # HH:mm
                            setattr(drama, key, f"1970-01-01 {value}:00")
                        elif len(value) <= 8: # HH:mm:ss
                            setattr(drama, key, f"1970-01-01 {value}")
                        else:
                            setattr(drama, key, value)
                    else:
                        setattr(drama, key, value)
            
            drama.save()
            return jsonify({"message": "success"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @classmethod
    def update_drama_status(cls, drama_id):
        # Implementation depends on what 'status' means, usually it's a soft delete or visibility toggle
        # For now, let's just placeholder it
        return jsonify({"message": "Status updated"}), 200

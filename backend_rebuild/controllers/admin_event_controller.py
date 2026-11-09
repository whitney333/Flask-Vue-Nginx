from flask import jsonify, request
from services.admin_event_service import OfflineEventService


class AdminEventController:
    def __init__(self, admin):
        self.admin = admin

    @classmethod
    def get_events(cls):
        try:
            page = request.args.get("page", 1)
            limit = request.args.get("limit", 10)
            search = request.args.get("search")

            result = OfflineEventService.get_events(page=page, limit=limit, search=search)

            return jsonify({
                "message": "success",
                **result
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @classmethod
    def get_event(cls, event_id):
        try:
            event = OfflineEventService.get_event(event_id)
            if not event:
                return jsonify({"error": "Event not found"}), 404

            return jsonify({
                "message": "success",
                "data": event
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @classmethod
    def create_event(cls):
        try:
            data = request.get_json() or {}
            event = OfflineEventService.create_event(data, getattr(request, "current_user", None))

            return jsonify({
                "message": "Event created successfully",
                "data": event
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @classmethod
    def update_event(cls, event_id):
        try:
            data = request.get_json() or {}
            event = OfflineEventService.update_event(event_id, data, getattr(request, "current_user", None))
            if not event:
                return jsonify({"error": "Event not found"}), 404

            return jsonify({
                "message": "Event updated successfully",
                "data": event
            }), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @classmethod
    def delete_event(cls, event_id):
        try:
            deleted = OfflineEventService.delete_event(event_id)
            if not deleted:
                return jsonify({"error": "Event not found"}), 404

            return jsonify({
                "message": "Event deleted successfully"
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_snapshots(event_id):
        try:
            snapshots = OfflineEventService.get_snapshots(event_id)
            return jsonify({"status": "success", "data": snapshots}), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 400

    @staticmethod
    def create_snapshot(event_id):
        try:
            data = request.get_json() or {}
            current_user = getattr(request, "current_user", None)
            snapshot = OfflineEventService.create_snapshot(event_id, data, current_user)
            return jsonify({"status": "success", "data": snapshot}), 201
        except ValueError as err:
            return jsonify({"error": str(err)}), 400
        except Exception as err:
            return jsonify({"error": str(err)}), 500

    @staticmethod
    def delete_snapshot(snapshot_id):
        try:
            success = OfflineEventService.delete_snapshot(snapshot_id)
            if not success:
                return jsonify({"error": "Snapshot not found"}), 404
            return jsonify({"status": "success", "message": "Snapshot deleted successfully"}), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 500
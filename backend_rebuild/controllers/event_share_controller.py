import logging
from typing import Tuple

from flask import Response, jsonify

from services.event_share_service import EventShareService

logger = logging.getLogger(__name__)

# One message for unknown, malformed and revoked tokens so links cannot be probed.
INVALID_LINK_MESSAGE = "This link is invalid or has expired."

PUBLIC_RESPONSE_HEADERS = {
    "Cache-Control": "no-store",
    "X-Robots-Tag": "noindex, nofollow",
    "Referrer-Policy": "no-referrer",
}


def _with_public_headers(response: Response) -> Response:
    for name, value in PUBLIC_RESPONSE_HEADERS.items():
        response.headers[name] = value
    return response


class EventShareController:
    # Admin (routes are protected by @admin_required)
    @staticmethod
    def create_share_link(event_id: str) -> Tuple[Response, int]:
        try:
            link = EventShareService.create_share_link(event_id)
            if not link:
                return jsonify({"success": False, "error": "Event not found"}), 404
            return jsonify({"success": True, "data": link}), 201
        except Exception:
            logger.exception("Failed to create share link for event %s", event_id)
            return jsonify({"success": False, "error": "Failed to create share link"}), 500

    @staticmethod
    def get_share_link(event_id: str) -> Tuple[Response, int]:
        try:
            link = EventShareService.get_share_link(event_id)
            if link is None:
                return jsonify({"success": False, "error": "Event not found"}), 404
            return jsonify({"success": True, "data": link}), 200
        except Exception:
            logger.exception("Failed to load share link for event %s", event_id)
            return jsonify({"success": False, "error": "Failed to load share link"}), 500

    @staticmethod
    def revoke_share_link(event_id: str) -> Tuple[Response, int]:
        try:
            if not EventShareService.revoke_share_link(event_id):
                return jsonify({"success": False, "error": "Event not found"}), 404
            return jsonify({"success": True, "data": None}), 200
        except Exception:
            logger.exception("Failed to revoke share link for event %s", event_id)
            return jsonify({"success": False, "error": "Failed to revoke share link"}), 500

    # Public (no auth: possession of the token is the credential)
    @staticmethod
    def get_public_report(token: str) -> Tuple[Response, int]:
        try:
            report = EventShareService.get_public_report(token)
        except Exception:
            # Never log the token itself: it is a bearer credential.
            logger.exception("Failed to load shared event report")
            response = jsonify({"success": False, "error": "Something went wrong. Please try again later."})
            return _with_public_headers(response), 500

        if not report:
            response = jsonify({"success": False, "error": INVALID_LINK_MESSAGE})
            return _with_public_headers(response), 404

        return _with_public_headers(jsonify({"success": True, "data": report})), 200

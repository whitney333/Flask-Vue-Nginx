"""Public, unauthenticated routes. Every route here must be safe to expose to anyone holding the link."""
from flask import Blueprint

from controllers.event_share_controller import EventShareController

share_bp = Blueprint("share", __name__)


@share_bp.route("/v1/events/<string:token>", methods=["GET"])
def get_shared_event_report(token):
    return EventShareController.get_public_report(token)

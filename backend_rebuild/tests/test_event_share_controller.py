"""Admin share controller, exercised directly (the @admin_required gate is covered in the route tests)."""
from flask import Flask

from controllers.event_share_controller import EventShareController
from models.event_model import OfflineEvent
from services.admin_event_service import OfflineEventService

MISSING_EVENT_ID = "0123456789abcdef01234567"


def _call(fn, *args):
    app = Flask(__name__)
    with app.test_request_context():
        response, status = fn(*args)
        return response.get_json(), status


def test_create_returns_201_with_token(event):
    body, status = _call(EventShareController.create_share_link, str(event.id))

    assert status == 201
    assert body["success"] is True
    token = body["data"]["share_token"]
    assert OfflineEvent.objects(id=event.id).first().share_token == token


def test_get_returns_the_active_link(event):
    created, _ = _call(EventShareController.create_share_link, str(event.id))

    body, status = _call(EventShareController.get_share_link, str(event.id))

    assert status == 200
    assert body == {"success": True, "data": created["data"]}


def test_get_returns_empty_link_when_none_is_active(event):
    body, status = _call(EventShareController.get_share_link, str(event.id))

    assert status == 200
    assert body["data"] == {"share_token": None, "share_token_created_at": None}


def test_get_returns_404_for_missing_event():
    body, status = _call(EventShareController.get_share_link, MISSING_EVENT_ID)

    assert status == 404
    assert body == {"success": False, "error": "Event not found"}


def test_create_returns_404_for_missing_event():
    body, status = _call(EventShareController.create_share_link, MISSING_EVENT_ID)

    assert status == 404
    assert body == {"success": False, "error": "Event not found"}


def test_revoke_returns_200_and_clears_token(event):
    _call(EventShareController.create_share_link, str(event.id))

    body, status = _call(EventShareController.revoke_share_link, str(event.id))

    assert status == 200
    assert body["success"] is True
    assert OfflineEvent.objects(id=event.id).first().share_token is None


def test_revoke_returns_404_for_missing_event():
    _, status = _call(EventShareController.revoke_share_link, MISSING_EVENT_ID)

    assert status == 404


def test_admin_event_payload_reports_link_status_but_never_the_token(event):
    body, _ = _call(EventShareController.create_share_link, str(event.id))

    payload = OfflineEventService.get_event(str(event.id))

    assert payload["has_share_link"] is True
    assert payload["share_token_created_at"] is not None
    assert "share_token" not in payload
    assert body["data"]["share_token"] not in str(payload)


def test_admin_event_payload_without_link(event):
    payload = OfflineEventService.get_event(str(event.id))

    assert payload["has_share_link"] is False
    assert payload["share_token_created_at"] is None

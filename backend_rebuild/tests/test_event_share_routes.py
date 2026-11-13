import pytest
from flask import Flask

from models.event_model import OfflineEvent
from routes.admin_route import admin_bp
from routes.share_route import share_bp
from services.event_share_service import EventShareService


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(share_bp, url_prefix="/api/share")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    return app.test_client()


def _public_url(token):
    return f"/api/share/v1/events/{token}"


def _stored_token(event):
    return OfflineEvent.objects(id=event.id).first().share_token


class TestPublicShareEndpoint:
    def test_valid_token_returns_report(self, client, event, closed_snapshot):
        token = EventShareService.create_share_link(str(event.id))["share_token"]

        response = client.get(_public_url(token))

        assert response.status_code == 200
        body = response.get_json()
        assert body["success"] is True
        assert body["data"]["event"]["event_name"] == "NOVA Fan Meeting Tour"

    def test_sets_privacy_headers(self, client, event):
        token = EventShareService.create_share_link(str(event.id))["share_token"]

        response = client.get(_public_url(token))

        assert response.headers["Cache-Control"] == "no-store"
        assert response.headers["X-Robots-Tag"] == "noindex, nofollow"
        assert response.headers["Referrer-Policy"] == "no-referrer"

    def test_unknown_and_malformed_tokens_get_identical_404(self, client, event):
        EventShareService.create_share_link(str(event.id))

        unknown = client.get(_public_url(EventShareService.generate_token()))
        malformed = client.get(_public_url("nope"))

        assert unknown.status_code == malformed.status_code == 404
        assert unknown.get_json() == malformed.get_json() == {
            "success": False,
            "error": "This link is invalid or has expired.",
        }
        assert malformed.headers["Cache-Control"] == "no-store"

    def test_revoked_token_returns_404(self, client, event):
        token = EventShareService.create_share_link(str(event.id))["share_token"]
        EventShareService.revoke_share_link(str(event.id))

        assert client.get(_public_url(token)).status_code == 404

    def test_unexpected_error_does_not_leak_details(self, client, monkeypatch):
        def boom(_token):
            raise RuntimeError("mongo://secret-host exploded")

        monkeypatch.setattr(EventShareService, "get_public_report", staticmethod(boom))

        response = client.get(_public_url(EventShareService.generate_token()))

        assert response.status_code == 500
        assert "secret-host" not in response.get_data(as_text=True)


class TestAdminShareEndpointsRequireAuth:
    @pytest.mark.parametrize("method", ["get", "post", "delete"])
    def test_rejects_unauthenticated_requests(self, client, event, method):
        response = getattr(client, method)(f"/api/admin/v1/events/{event.id}/share")

        assert response.status_code == 401
        assert _stored_token(event) is None

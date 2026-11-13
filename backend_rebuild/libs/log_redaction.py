"""Strip share-link tokens from log lines: the token in the URL is a bearer credential."""
import re
from typing import Any, Mapping

REDACTED = "[REDACTED]"

# Matches both the API path (/api/share/v1/events/<token>) and the SPA path (/share/events/<token>).
_SHARE_TOKEN_IN_PATH = re.compile(r"(/share/(?:v1/)?events/)[A-Za-z0-9_-]+")


def redact_share_tokens(text: str) -> str:
    return _SHARE_TOKEN_IN_PATH.sub(rf"\g<1>{REDACTED}", text)


def redact_atoms(atoms: Mapping[str, Any]) -> dict:
    """Return a copy of a gunicorn access-log atoms dict with every string value redacted."""
    return {
        key: redact_share_tokens(value) if isinstance(value, str) else value
        for key, value in atoms.items()
    }

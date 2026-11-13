from libs.log_redaction import REDACTED, redact_atoms, redact_share_tokens

TOKEN = "Abc123_-" * 5 + "xyz"  # 43 chars, same alphabet as real tokens


def test_redacts_api_share_path():
    line = f"GET /api/share/v1/events/{TOKEN} HTTP/1.1"

    assert redact_share_tokens(line) == f"GET /api/share/v1/events/{REDACTED} HTTP/1.1"


def test_redacts_spa_share_path_and_query():
    assert redact_share_tokens(f"/share/events/{TOKEN}?x=1") == f"/share/events/{REDACTED}?x=1"


def test_leaves_unrelated_paths_untouched():
    line = "GET /api/admin/v1/events/0123456789abcdef01234567/share HTTP/1.1"

    assert redact_share_tokens(line) == line


def test_redact_atoms_returns_new_dict_with_string_values_redacted():
    atoms = {"r": f"GET /api/share/v1/events/{TOKEN} HTTP/1.1", "U": f"/api/share/v1/events/{TOKEN}", "s": 200}

    result = redact_atoms(atoms)

    assert TOKEN not in str(result)
    assert result["s"] == 200
    assert TOKEN in atoms["U"], "input must not be mutated"

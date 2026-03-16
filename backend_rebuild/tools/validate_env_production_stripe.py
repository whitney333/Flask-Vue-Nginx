import argparse
import os
import sys
from urllib.parse import urlparse

from dotenv import dotenv_values


REQUIRED_KEYS = [
    "STRIPE_SECRET_KEY",
    "STRIPE_WEBHOOK_SECRET",
    "FRONTEND_URL",
    "STRIPE_PRICE_STARTER_MONTHLY",
    "STRIPE_PRICE_STARTER_YEARLY",
    "STRIPE_PRICE_STANDARD_MONTHLY",
    "STRIPE_PRICE_STANDARD_YEARLY",
]


def _mask(value: str, keep_start: int = 8, keep_end: int = 4) -> str:
    if not value:
        return ""
    if len(value) <= keep_start + keep_end:
        return "***"
    return f"{value[:keep_start]}...{value[-keep_end:]}"


def _is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except Exception:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _detect_mode(secret_key: str) -> str:
    if secret_key.startswith("sk_live_"):
        return "live"
    if secret_key.startswith("sk_test_"):
        return "test"
    return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate backend_rebuild/.env.production Stripe-related settings."
    )
    parser.add_argument(
        "--env-file",
        default=os.path.join(os.path.dirname(__file__), "..", ".env.production"),
        help="Path to dotenv file (default: backend_rebuild/.env.production)",
    )
    parser.add_argument(
        "--verify-api",
        action="store_true",
        help="Also call Stripe API to verify key + price ids (requires network).",
    )
    args = parser.parse_args()

    env_file = os.path.abspath(args.env_file)
    if not os.path.exists(env_file):
        print(f"[FAIL] env file not found: {env_file}")
        return 2

    values = dotenv_values(env_file)

    missing = [k for k in REQUIRED_KEYS if not (values.get(k) or "").strip()]
    if missing:
        print("[FAIL] Missing required keys:")
        for k in missing:
            print(f"  - {k}")
        return 3

    stripe_secret = (values.get("STRIPE_SECRET_KEY") or "").strip()
    webhook_secret = (values.get("STRIPE_WEBHOOK_SECRET") or "").strip()
    frontend_url = (values.get("FRONTEND_URL") or "").strip()
    price_ids = {
        "starter_monthly": (values.get("STRIPE_PRICE_STARTER_MONTHLY") or "").strip(),
        "starter_yearly": (values.get("STRIPE_PRICE_STARTER_YEARLY") or "").strip(),
        "standard_monthly": (values.get("STRIPE_PRICE_STANDARD_MONTHLY") or "").strip(),
        "standard_yearly": (values.get("STRIPE_PRICE_STANDARD_YEARLY") or "").strip(),
    }

    problems: list[str] = []
    warnings: list[str] = []

    mode = _detect_mode(stripe_secret)
    if mode == "unknown":
        problems.append("STRIPE_SECRET_KEY does not start with sk_live_ or sk_test_.")

    if not webhook_secret.startswith("whsec_"):
        warnings.append("STRIPE_WEBHOOK_SECRET does not start with whsec_.")

    for name, pid in price_ids.items():
        if not pid.startswith("price_"):
            problems.append(f"{name} price id does not start with price_.")

    if not _is_valid_url(frontend_url):
        problems.append("FRONTEND_URL is not a valid http(s) URL.")
    else:
        if mode == "live" and frontend_url.startswith("http://"):
            warnings.append("Live Stripe key with http FRONTEND_URL; consider https in production.")

    print("[OK] Required keys present.")
    print(f"[INFO] STRIPE_SECRET_KEY mode: {mode} ({_mask(stripe_secret)})")
    print(f"[INFO] STRIPE_WEBHOOK_SECRET: {_mask(webhook_secret)}")
    print(f"[INFO] FRONTEND_URL: {frontend_url}")
    for name, pid in price_ids.items():
        print(f"[INFO] {name}: {pid}")

    if warnings:
        print("[WARN] Warnings:")
        for w in warnings:
            print(f"  - {w}")

    if problems:
        print("[FAIL] Problems:")
        for p in problems:
            print(f"  - {p}")
        return 4

    if args.verify_api:
        try:
            import stripe  # noqa: PLC0415
        except Exception as e:
            print(f"[FAIL] Cannot import stripe library: {e}")
            return 5

        try:
            stripe.api_key = stripe_secret
            acct = stripe.Account.retrieve()
            print(f"[OK] Stripe API key verified. account_id={acct.get('id')}")
        except Exception as e:
            # Network-restricted environments commonly fail here; still surface the error.
            print(f"[FAIL] Stripe API key verification failed: {type(e).__name__}: {e}")
            return 6

        for name, pid in price_ids.items():
            try:
                price = stripe.Price.retrieve(pid)
                print(f"[OK] Price id verified: {name}={price.get('id')}")
            except Exception as e:
                print(f"[FAIL] Price id verification failed: {name} ({pid}): {type(e).__name__}: {e}")
                return 7

    print("[OK] Stripe .env.production looks runnable for backend_rebuild.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


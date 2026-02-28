from __future__ import annotations

import random
from pathlib import Path

import pandas as pd

BENIGN_DOMAINS = [
    "google.com",
    "github.com",
    "microsoft.com",
    "wikipedia.org",
    "linkedin.com",
    "stackoverflow.com",
    "amazon.com",
    "apple.com",
    "cloudflare.com",
    "kaggle.com",
    "openai.com",
    "react.dev",
]

BENIGN_PATHS = [
    "",
    "/docs",
    "/blog",
    "/support",
    "/pricing",
    "/about",
    "/products",
    "/security",
    "/learn",
    "/account/settings",
]

MALICIOUS_PREFIX = [
    "secure-login",
    "verify-account",
    "urgent-update",
    "free-bonus",
    "confirm-payment",
    "bank-alert",
    "wallet-recovery",
    "password-reset",
    "invoice-overdue",
    "suspended-session",
]

MALICIOUS_SUFFIX = [".ru", ".xyz", ".click", ".top", ".info", ".site", ".biz", ".work"]

MALICIOUS_PATHS = [
    "/login",
    "/auth/verify",
    "/account/check",
    "/download/setup.exe",
    "/invoice/view",
    "/password/reset",
    "/secure/update",
    "/billing/confirm",
]


def make_good_url() -> str:
    scheme = random.choice(["https", "https", "https", "http"])
    domain = random.choice(BENIGN_DOMAINS)
    path = random.choice(BENIGN_PATHS)
    query = ""
    if random.random() < 0.18:
        query = f"?ref={random.choice(['home', 'app', 'profile', 'docs'])}"
    return f"{scheme}://{domain}{path}{query}"


def make_bad_url() -> str:
    scheme = random.choice(["http", "http", "https"])
    host = f"{random.choice(MALICIOUS_PREFIX)}-{random.choice(['secure', 'alert', 'verify', 'auth'])}{random.choice(MALICIOUS_SUFFIX)}"
    path = random.choice(MALICIOUS_PATHS)
    if random.random() < 0.2:
        path = f"/{random.randint(10, 222)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}{path}"
    if random.random() < 0.25:
        path += random.choice(["?session=expired", "?token=verify", "?step=confirm"])
    return f"{scheme}://{host}{path}"


def build_dataset(size_per_class: int = 20000) -> pd.DataFrame:
    rows = [[make_good_url(), "good"] for _ in range(size_per_class)]
    rows += [[make_bad_url(), "bad"] for _ in range(size_per_class)]
    random.shuffle(rows)
    df = pd.DataFrame(rows, columns=["url", "label"]).drop_duplicates()
    return df


def main() -> None:
    random.seed(42)
    df = build_dataset(size_per_class=20000)
    out_path = Path(__file__).with_name("urls_large.csv")
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df):,} rows to {out_path}")


if __name__ == "__main__":
    main()

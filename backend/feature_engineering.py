from __future__ import annotations

import re
from typing import List

SUSPICIOUS_TOKENS = [
    "login",
    "verify",
    "update",
    "secure",
    "account",
    "password",
    "bank",
    "free",
    "bonus",
    "confirm",
]


def extract_struct_features(url: str) -> List[float]:
    url = url.strip()
    length = len(url)
    digit_count = sum(ch.isdigit() for ch in url)
    has_https = 1.0 if url.lower().startswith("https") else 0.0
    has_ip = 1.0 if re.search(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", url) else 0.0
    has_at = 1.0 if "@" in url else 0.0
    has_exe = 1.0 if ".exe" in url.lower() else 0.0
    has_dash = url.count("-")
    dot_count = url.count(".")
    slash_count = url.count("/")
    query_count = url.count("?") + url.count("=") + url.count("&")
    subdomain_count = max(dot_count - 1, 0)
    token_hits = sum(1 for token in SUSPICIOUS_TOKENS if token in url.lower())

    return [
        float(length),
        float(digit_count),
        float(has_https),
        float(has_ip),
        float(has_at),
        float(has_exe),
        float(has_dash),
        float(dot_count),
        float(slash_count),
        float(query_count),
        float(subdomain_count),
        float(token_hits),
    ]

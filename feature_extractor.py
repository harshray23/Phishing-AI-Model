import joblib
import math
import re
from urllib.parse import urlparse

# Load training feature names
FEATURE_NAMES = joblib.load("features.pkl")

def extract_features(url: str) -> dict:
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    features = {}

    # ---------------- BASIC FEATURES (you already had) ----------------
    features["uses_https"] = int(parsed.scheme == "https")
    features["digit_in_domain"] = int(any(c.isdigit() for c in domain))
    features["repeated_chars"] = int(bool(re.search(r"(.)\1{2,}", domain)))
    features["ssl_words"] = int(any(w in domain for w in ["secure", "login", "verify"]))
    features["min_brand_similarity"] = 0.0  # placeholder if needed

    # ---------------- STRUCTURAL FEATURES ----------------
    features["domain_length"] = len(domain)
    features["subdomain_count"] = domain.count(".") - 1
    features["dot_count"] = domain.count(".")
    features["dash_count"] = domain.count("-")
    features["digit_ratio"] = sum(c.isdigit() for c in domain) / max(len(domain), 1)
    features["has_ip_domain"] = int(bool(re.match(r"\d+\.\d+\.\d+\.\d+", domain)))
    features["domain_entropy"] = _entropy(domain)

    # ---------------- ADVERSARIAL / UNICODE ----------------
    features["has_unicode"] = int(any(ord(c) > 127 for c in domain))
    features["is_punycode"] = int(domain.startswith("xn--"))
    features["homoglyph_detected"] = 0  # placeholder
    features["normalized_brand_match"] = 0

    # ---------------- CANONICALIZATION ----------------
    features["canonical_changed"] = 0
    features["canonical_length_diff"] = 0
    features["canonical_brand_similarity"] = 0
    features["canonical_brand_match"] = 0

    # ---------------- SLD FEATURES ----------------
    sld = domain.split(".")[0]
    features["sld_length"] = len(sld)
    features["sld_has_digit"] = int(any(c.isdigit() for c in sld))
    features["sld_digit_substitution"] = 0
    features["sld_brand_similarity"] = 0
    features["sld_brand_match"] = 0

    # ---------------- SUSPICIOUS TLD ----------------
    features["suspicious_tld"] = int(domain.endswith((".tk", ".ml", ".ga", ".cf")))

    # ---------------- FINAL GUARANTEE ----------------
    # Ensure ALL training features exist
    final_features = {f: float(features.get(f, 0)) for f in FEATURE_NAMES}

    return final_features


def _entropy(s: str) -> float:
    probs = [s.count(c) / len(s) for c in set(s)] if s else [1]
    return -sum(p * math.log2(p) for p in probs)

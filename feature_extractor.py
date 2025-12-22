def extract_features(url):
    return {
        # existing
        "min_brand_similarity": ...,
        "repeated_chars": ...,
        "digit_in_domain": ...,
        "uses_https": ...,
        "ssl_words": ...,
        "domain_length": ...,
        "subdomain_count": ...,
        "has_ip_domain": ...,
        "suspicious_tld": ...,
        "domain_entropy": ...,
        "dot_count": ...,
        "dash_count": ...,
        "digit_ratio": ...,

        # NEW (can start simple)
        "homoglyph_detected": 0,
        "normalized_brand_match": 0,
        "has_unicode": int(any(ord(c) > 127 for c in url)),
        "is_punycode": int("xn--" in url),
        "canonical_changed": 0,
        "canonical_length_diff": 0,
        "canonical_brand_similarity": 0,
        "canonical_brand_match": 0,
        "sld_length": 0,
        "sld_has_digit": 0,
        "sld_digit_substitution": 0,
        "sld_brand_similarity": 0,
        "sld_brand_match": 0
    }

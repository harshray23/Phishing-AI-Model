import whois
import socket
import datetime

def get_whois_features(domain):
    features = {
        "domain_age_days": 0,
        "is_new_domain": 1
    }
    try:
        w = whois.whois(domain)
        if w.creation_date:
            creation = w.creation_date
            if isinstance(creation, list):
                creation = creation[0]
            age = (datetime.datetime.now() - creation).days
            features["domain_age_days"] = max(age, 0)
            features["is_new_domain"] = 1 if age < 180 else 0
    except:
        pass
    return features

def get_dns_features(domain):
    features = {
        "has_dns": 0,
        "ip_count": 0
    }
    try:
        infos = socket.getaddrinfo(domain, None)
        features["has_dns"] = 1
        features["ip_count"] = len(set([i[4][0] for i in infos]))
    except:
        pass
    return features

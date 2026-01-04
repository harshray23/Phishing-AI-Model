import asyncio
import socket
from urllib.parse import urlparse

async def resolve_dns(domain):
    loop = asyncio.get_event_loop()
    try:
        await loop.getaddrinfo(domain, None)
        return 1
    except:
        return 0

async def extract_features_async(url):
    parsed = urlparse(url)
    domain = parsed.netloc

    has_ip = any(char.isdigit() for char in domain)
    has_https = parsed.scheme == "https"

    return {
        "url_length": len(url),
        "digit_count": sum(c.isdigit() for c in url),
        "has_ip": int(has_ip),
        "has_https": int(has_https),
        "has_dns": await resolve_dns(domain),
    }

import asyncio
import re
from urllib.parse import urlparse
import whois

async def resolve_dns(domain: str) -> int:
    try:
        loop = asyncio.get_event_loop()
        await loop.getaddrinfo(domain, None)
        return 1
    except:
        return 0

async def get_domain_age(domain: str) -> int:
    try:
        data = await asyncio.to_thread(whois.whois, domain)
        if data.creation_date:
            if isinstance(data.creation_date, list):
                return (data.creation_date[0]).year
            return data.creation_date.year
    except:
        pass
    return 0

async def extract_features_async(url: str) -> dict:
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    dns_task = asyncio.create_task(resolve_dns(domain))
    whois_task = asyncio.create_task(get_domain_age(domain))

    return {
        "url_length": len(url),
        "digit_count": sum(c.isdigit() for c in url),
        "has_ip": int(bool(re.search(r"\d+\.\d+\.\d+\.\d+", domain))),
        "has_hyphen": int("-" in domain),
        "has_https": int(parsed.scheme == "https"),
        "has_dns": await dns_task,
        "domain_age": await whois_task,
    }

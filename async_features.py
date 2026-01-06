import asyncio
import socket
from urllib.parse import urlparse

async def resolve_dns(domain):
    try:
        loop = asyncio.get_event_loop()
        await asyncio.wait_for(
            loop.getaddrinfo(domain, None),
            timeout=3
        )
        return 1
    except:
        return 0


async def get_whois_age(domain):
    try:
        data = await asyncio.wait_for(
            asyncio.to_thread(whois.whois, domain),
            timeout=5
        )
        if data.creation_date:
            if isinstance(data.creation_date, list):
                return data.creation_date[0].year
            return data.creation_date.year
    except:
        return 0

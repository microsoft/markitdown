"""Rate limiting middleware."""

import time
from collections import defaultdict
from fastapi import Request, HTTPException
from .config import Settings

# Store request counts per IP, structured as:
# {ip_address: [(timestamp, count), ...]}
request_store = defaultdict(list)


def cleanup_old_requests(ip: str, window: int = 60) -> None:
    """Remove requests older than the window."""
    current = time.time()
    request_store[ip] = [
        (ts, count)
        for ts, count in request_store[ip]
        if current - ts < window
    ]


async def rate_limit_middleware(request: Request, settings: Settings):
    """Rate limiting middleware."""
    ip = request.client.host
    current = time.time()

    # Clean up old requests
    cleanup_old_requests(ip)

    # Count requests in the current window
    total = sum(count for _, count in request_store[ip])

    if total >= settings.rate_limit:
        raise HTTPException(
            status_code=429,
            detail="Too many requests",
        )

    # Add current request
    request_store[ip].append((current, 1))
import re
from fastapi import Request

CONTENT_POLICY = "default-src 'none'"


async def content_policy(request: Request, call_next):
    response = await call_next(request)
    if not request.url.path.startswith("/docs"):
        response.headers["Content-Security-Policy"] = CONTENT_POLICY
    return response

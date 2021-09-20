from fastapi import Request

CONTENT_POLICY = "default-src 'none'"


async def content_policy(request: Request, call_next):
    response = await call_next(request)
    request.url.path.split("/")[-1]
    if not request.url.path.split("/")[-1].startswith("docs"):
        response.headers["Content-Security-Policy"] = CONTENT_POLICY
    return response

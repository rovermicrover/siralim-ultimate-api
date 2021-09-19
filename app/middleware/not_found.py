from fastapi import Request
from sqlalchemy.exc import NoResultFound
from starlette.responses import JSONResponse


async def not_found(request: Request, call_next):
    try:
        response = await call_next(request)
    except NoResultFound:
        return JSONResponse(
            status_code=404,
            content={"detial": "Item not found"},
        )

    return response

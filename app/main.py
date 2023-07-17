from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.api import user

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"{exc.detail}"},
    )


app.include_router(user.router, prefix="/users", tags=["users"])

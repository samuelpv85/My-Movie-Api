from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse


class ErrorHandle(BaseHTTPMiddleware):
    # metodoContructor(se le pasa una aplicacion FastAPI)
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    # Detecta si ocurre un error en la app
    async def dispatch(
        self, request: Request, call_next
    ) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": str(e)})

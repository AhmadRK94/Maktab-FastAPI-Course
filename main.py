from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.expenses.routes import router as expenses_router
from app.users.routes import router as users_router
from app.auth.routes import router as auth_router
from app.core.config import settings
import sentry_sdk


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Startup.")
    yield
    print("Application Shutdown.")


app = FastAPI(lifespan=lifespan)
app.include_router(expenses_router)
app.include_router(users_router)
app.include_router(auth_router)

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    send_default_pii=True,
)


@app.get("/readiness")
def readiness():
    return JSONResponse(content="ok", status_code=200)


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


@app.exception_handler(HTTPException)
def custom_http_exception(request: Response, exc: HTTPException):
    content = {"error": True, "status_code": exc.status_code, "detail": str(exc.detail)}
    return JSONResponse(status_code=exc.status_code, content=content)

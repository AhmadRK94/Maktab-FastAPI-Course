from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.expenses.routes import router as expenses_router
from app.users.routes import router as users_router
from app.auth.routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Startup.")
    yield
    print("Application Shutdown.")


app = FastAPI(lifespan=lifespan)
app.include_router(expenses_router)
app.include_router(users_router)
app.include_router(auth_router)

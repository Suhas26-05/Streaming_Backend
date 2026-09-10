from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.database import Base, engine
from app.routers.admin import router as admin_router
from app.routers.auth import router as auth_router
from app.routers.user import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI application is starting...")
    try:
        with engine.connect() as connection:
            if connection.execute(text("SELECT 1")).scalar() == 1: print("Successfully connected to SQL Server!")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise
    yield
    print("FastAPI application is shutting down...")
    engine.dispose()
    print("Database connection pool closed.")

Base.metadata.create_all(bind=engine)
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home(): 
    return {"message": "FastAPI is running"}

app.include_router(user_router)
app.include_router(admin_router)
app.include_router(auth_router)

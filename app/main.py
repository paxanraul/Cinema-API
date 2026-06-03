from fastapi import FastAPI

from app.routers import auth


app = FastAPI(
    title="CinemaAPI",
    description="Backend API for cinema service",
    version="0.1.0"
)


app.include_router(auth.router)
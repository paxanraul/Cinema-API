from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers import auth, sessions, bookings, movies
from app.db.session import SessionLocal
from app.middleware.logging import log_requests


@asynccontextmanager
async def lifespan(app: FastAPI):
	db = SessionLocal()
	try:
		yield
	finally:
		db.close()		


app = FastAPI(
    title="CinemaAPI",
    description="Backend API for cinema service",
    version="0.1.0",
    lifespan=lifespan
)

app.middleware("http")(log_requests)

app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(bookings.router)
app.include_router(movies.router)

@app.get("/health")
def get_health():
	return {"status": "ok"}
from contextlib import asynccontextmanager
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.routers import auth, sessions, bookings, movies, halls
from app.db.session import SessionLocal
from app.db.seed import run_seed
from app.middleware.logging import log_requests
from app.core.limiter import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
	db = SessionLocal()
	try:
		run_seed(db)
	finally:
		db.close()		


app = FastAPI(
    title="CinemaAPI",
    description="Backend API for cinema service",
    version="0.1.0",
    lifespan=lifespan
)

#rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

#middleware
app.middleware("http")(log_requests)

#routers
app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(bookings.router)
app.include_router(movies.router)
app.include_router(halls.router)

@app.get("/health")
def get_health():
	return {"status": "ok"}
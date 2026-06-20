from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.session import SessionCreate, SessionResponse
from app.services.session_service import create_session, get_session


router = APIRouter(
	prefix="/sessions",
	tags=["sessions"]
)

@router.get("/get_sessions", response_model=list[SessionResponse])
def get_sessions(
	db: Session = Depends(get_db),
	current_user: User = Depends(get_current_user)
):
	sessions = get_session(db, current_user.id)
	return sessions


@router.post("/create_session", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def add_session(
	session_data: SessionCreate,
	current_user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
):
	sessions = create_session(db, session_data)
	return sessions
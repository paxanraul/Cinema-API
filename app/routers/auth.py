from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import Login, TokenResponse
from app.schemas.user import UserRegister, UserResponse
from app.services.user_service import (
    get_user_by_email,
    create_user,
    deactivate_user,
    authenticate_user
)
from app.models.user import User
from app.dependencies.auth import get_current_user
from app.core.security import create_access_token, decode_access_token
from app.core.config import settings


router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)    
):
    if user_data.password != user_data.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    existing_user = get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = create_user(db, user_data)
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    login_data: Login,
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, login_data.email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return TokenResponse(access_token=access_token)


@router.patch("/deactivate")
def deactivate_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deactivate_account(db, current_user)

    return {"detail": "Account deactivated successfully"}
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
import bcrypt

from app.core.config import settings

# Functions for work with passwords

def hash_password(password: str) -> str:
    """Hashes a clean password using a salt"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies the match of a clean and hashed password"""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# Functions for work with jwt token

def create_access_token(data: dict, expires_delta: Optional[timedelta]):
    """Generate a secure JSON web token (jwt)"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """Decodes and validates the JWT token"""
    try:
        return jwt.encode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except jwt.PyJWTError:
        return None
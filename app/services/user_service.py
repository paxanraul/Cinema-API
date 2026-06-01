from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserRegister
from app.core.security import hash_password, verify_password

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_data: UserRegister) -> User:
    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        patronymic=user_data.patronymic,
        email=user_data.email,
        hash_password=hash_password(user_data.password),
        role="user",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)

    if not user:
        return None
    
    if not verify_password(password, user.hash_password):
        return None
    
    return user

def deactivate_user(db: Session, user: User) -> User:
    user.is_active = False
    db.commit()
    db.refresh(User)
    return user

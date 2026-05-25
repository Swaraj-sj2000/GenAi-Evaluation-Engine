#app/repositories/user_repo.py  

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate,UserResponse,LoginData
from app.utils.password_utils import hash_password

def create_user(db:Session,user_data:UserCreate)->UserResponse:
    db_user=User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(id=db_user.id,username=db_user.username)


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


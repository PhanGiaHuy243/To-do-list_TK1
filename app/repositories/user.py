from typing import Optional
from sqlalchemy.orm import Session
from app.core.models import UserModel
from app.schemas.auth import UserCreate
from app.core.security import hash_password

class UserRepository:
    """Repository quản lý dữ liệu user"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_email(self, email: str) -> Optional[UserModel]:
        """Lấy user theo email"""
        return self.db.query(UserModel).filter(UserModel.email == email).first()
    
    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        """Lấy user theo ID"""
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()
    
    def create(self, user_create: UserCreate) -> UserModel:
        """Tạo user mới"""
        db_user = UserModel(
            email=user_create.email,
            hashed_password=hash_password(user_create.password)
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

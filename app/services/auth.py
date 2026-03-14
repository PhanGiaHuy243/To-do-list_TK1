from sqlalchemy.orm import Session
from datetime import timedelta
from app.repositories.user import UserRepository
from app.schemas.auth import UserCreate, LoginRequest, User, TokenResponse
from app.core.security import (
    verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
)

class AuthService:
    """Service cho authentication"""
    
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
    
    def register(self, user_create: UserCreate) -> User:
        """Đăng ký user mới"""
        # Check if email already exists
        existing_user = self.user_repo.get_by_email(user_create.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Create user
        db_user = self.user_repo.create(user_create)
        return User.from_orm(db_user)
    
    def login(self, login_request: LoginRequest) -> TokenResponse:
        """Login và tạo JWT token"""
        # Find user
        db_user = self.user_repo.get_by_email(login_request.email)
        if not db_user:
            raise ValueError("Invalid email or password")
        
        # Verify password
        if not verify_password(login_request.password, db_user.hashed_password):
            raise ValueError("Invalid email or password")
        
        # Create token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(db_user.id), "email": db_user.email},
            expires_delta=access_token_expires
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=User.from_orm(db_user)
        )
    
    def get_user(self, user_id: int) -> User:
        """Lấy user theo ID"""
        db_user = self.user_repo.get_by_id(user_id)
        if not db_user:
            raise ValueError("User not found")
        return User.from_orm(db_user)

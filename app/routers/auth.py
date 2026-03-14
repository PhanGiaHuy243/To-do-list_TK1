from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.models import UserModel
from app.schemas.auth import UserCreate, LoginRequest, User, TokenResponse
from app.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register", response_model=TokenResponse)
def register(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """Đăng ký user mới"""
    service = AuthService(db)
    try:
        service.register(user_create)
        # Login ngay sau khi register
        login_request = LoginRequest(
            email=user_create.email,
            password=user_create.password
        )
        return service.login(login_request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=TokenResponse)
def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db)
):
    """Đăng nhập và lấy token"""
    service = AuthService(db)
    try:
        return service.login(login_request)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.get("/me", response_model=User)
def get_me(current_user: UserModel = Depends(get_current_user)):
    """Lấy thông tin user hiện tại"""
    return User.from_orm(current_user)

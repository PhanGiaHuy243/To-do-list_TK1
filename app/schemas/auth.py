from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Base user model"""
    email: EmailStr

class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=6, max_length=100)

class User(UserBase):
    """User response schema"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    """Login request"""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    token_type: str = "bearer"
    user: User

class TokenData(BaseModel):
    """Token data (from JWT)"""
    user_id: Optional[int] = None
    email: Optional[str] = None

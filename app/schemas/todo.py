from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TodoBase(BaseModel):
    """Base model cho Todo"""
    title: str = Field(..., min_length=3, max_length=100, description="Tiêu đề todo (3-100 ký tự)")
    description: Optional[str] = Field(None, max_length=500, description="Mô tả chi tiết")
    is_done: bool = False

class TodoCreate(TodoBase):
    """Model tạo todo mới"""
    pass

class TodoUpdate(TodoBase):
    """Model cập nhật todo (toàn bộ)"""
    pass

class TodoPartialUpdate(BaseModel):
    """Model cập nhật một phần (PATCH)"""
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_done: Optional[bool] = None

class Todo(TodoBase):
    """Model Todo đầy đủ"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TodoListResponse(BaseModel):
    """Response cho GET /todos"""
    items: list[Todo]
    total: int
    limit: int
    offset: int


from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class TagSchema(BaseModel):
    """Model cho Tag"""
    id: int
    name: str

    class Config:
        from_attributes = True

class TodoBase(BaseModel):
    """Base model cho Todo"""
    title: str = Field(..., min_length=3, max_length=100, description="Tiêu đề todo (3-100 ký tự)")
    description: Optional[str] = Field(None, max_length=500, description="Mô tả chi tiết")
    is_done: bool = False
    due_date: Optional[date] = Field(None, description="Ngày deadline")

class TodoCreate(TodoBase):
    """Model tạo todo mới"""
    tags: Optional[list[str]] = Field(None, description="Danh sách tên tags")

class TodoUpdate(TodoBase):
    """Model cập nhật todo (toàn bộ)"""
    tags: Optional[list[str]] = None

class TodoPartialUpdate(BaseModel):
    """Model cập nhật một phần (PATCH)"""
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_done: Optional[bool] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None

class Todo(TodoBase):
    """Model Todo đầy đủ"""
    id: int
    created_at: datetime
    updated_at: datetime
    tags: list[TagSchema] = []

    class Config:
        from_attributes = True

class TodoListResponse(BaseModel):
    """Response cho GET /todos"""
    items: list[Todo]
    total: int
    limit: int
    offset: int


from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.todo import (
    Todo, TodoCreate, TodoUpdate, TodoPartialUpdate, TodoListResponse
)
from app.repositories.todo import TodoRepository

class TodoService:
    """Service layer - chứa business logic"""
    
    def __init__(self, db: Session):
        self.repository = TodoRepository(db)
    
    def create_todo(self, owner_id: int, todo_create: TodoCreate) -> Todo:
        """Tạo todo mới"""
        db_todo = self.repository.create(owner_id, todo_create)
        return Todo.from_orm(db_todo)
    
    def get_todos(
        self,
        owner_id: int,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: str = "created_at",
        limit: int = 10,
        offset: int = 0
    ) -> TodoListResponse:
        """Lấy danh sách todos của user"""
        items, total = self.repository.get_all(
            owner_id=owner_id,
            is_done=is_done,
            q=q,
            sort=sort,
            limit=limit,
            offset=offset
        )
        return TodoListResponse(
            items=[Todo.from_orm(item) for item in items],
            total=total,
            limit=limit,
            offset=offset
        )
    
    def get_todo(self, todo_id: int, owner_id: int) -> Optional[Todo]:
        """Lấy todo theo ID"""
        db_todo = self.repository.get_by_id(todo_id, owner_id)
        return Todo.from_orm(db_todo) if db_todo else None
    
    def update_todo(self, todo_id: int, owner_id: int, todo_update: TodoUpdate) -> Optional[Todo]:
        """Cập nhật todo (toàn bộ)"""
        db_todo = self.repository.update(todo_id, owner_id, todo_update)
        return Todo.from_orm(db_todo) if db_todo else None
    
    def partial_update_todo(
        self, todo_id: int, owner_id: int, todo_update: TodoPartialUpdate
    ) -> Optional[Todo]:
        """Cập nhật một phần todo (PATCH)"""
        db_todo = self.repository.partial_update(todo_id, owner_id, todo_update)
        return Todo.from_orm(db_todo) if db_todo else None
    
    def delete_todo(self, todo_id: int, owner_id: int) -> Optional[Todo]:
        """Xóa todo"""
        db_todo = self.repository.delete(todo_id, owner_id)
        return Todo.from_orm(db_todo) if db_todo else None
    
    def get_overdue_todos(
        self, owner_id: int, limit: int = 10, offset: int = 0
    ) -> TodoListResponse:
        """Lấy todos quá hạn"""
        items, total = self.repository.get_overdue(owner_id, limit, offset)
        return TodoListResponse(
            items=[Todo.from_orm(item) for item in items],
            total=total,
            limit=limit,
            offset=offset
        )
    
    def get_today_todos(
        self, owner_id: int, limit: int = 10, offset: int = 0
    ) -> TodoListResponse:
        """Lấy todos hôm nay"""
        items, total = self.repository.get_today(owner_id, limit, offset)
        return TodoListResponse(
            items=[Todo.from_orm(item) for item in items],
            total=total,
            limit=limit,
            offset=offset
        )


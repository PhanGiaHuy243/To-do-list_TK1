from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.models import TodoModel
from app.schemas.todo import TodoCreate, TodoUpdate, TodoPartialUpdate

class TodoRepository:
    """Repository quản lý dữ liệu todo từ database"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, todo_create: TodoCreate) -> TodoModel:
        """Tạo todo mới"""
        db_todo = TodoModel(
            title=todo_create.title,
            description=todo_create.description,
            is_done=todo_create.is_done
        )
        self.db.add(db_todo)
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo
    
    def get_all(
        self,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: str = "created_at",
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[list[TodoModel], int]:
        """Lấy danh sách todos với filter, search, sort, pagination"""
        query = self.db.query(TodoModel)
        
        # Filter by is_done
        if is_done is not None:
            query = query.filter(TodoModel.is_done == is_done)
        
        # Search by title
        if q:
            query = query.filter(TodoModel.title.ilike(f"%{q}%"))
        
        # Get total
        total = query.count()
        
        # Sort
        if sort == "-created_at":
            query = query.order_by(desc(TodoModel.created_at))
        else:
            query = query.order_by(TodoModel.created_at)
        
        # Pagination
        items = query.offset(offset).limit(limit).all()
        
        return items, total
    
    def get_by_id(self, todo_id: int) -> Optional[TodoModel]:
        """Lấy todo theo ID"""
        return self.db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    
    def update(self, todo_id: int, todo_update: TodoUpdate) -> Optional[TodoModel]:
        """Cập nhật todo (toàn bộ)"""
        db_todo = self.get_by_id(todo_id)
        if db_todo:
            db_todo.title = todo_update.title
            db_todo.description = todo_update.description
            db_todo.is_done = todo_update.is_done
            self.db.commit()
            self.db.refresh(db_todo)
        return db_todo
    
    def partial_update(self, todo_id: int, todo_update: TodoPartialUpdate) -> Optional[TodoModel]:
        """Cập nhật một phần (PATCH)"""
        db_todo = self.get_by_id(todo_id)
        if db_todo:
            if todo_update.title is not None:
                db_todo.title = todo_update.title
            if todo_update.description is not None:
                db_todo.description = todo_update.description
            if todo_update.is_done is not None:
                db_todo.is_done = todo_update.is_done
            self.db.commit()
            self.db.refresh(db_todo)
        return db_todo
    
    def delete(self, todo_id: int) -> Optional[TodoModel]:
        """Xóa todo"""
        db_todo = self.get_by_id(todo_id)
        if db_todo:
            self.db.delete(db_todo)
            self.db.commit()
        return db_todo


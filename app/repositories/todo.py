from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.models import TodoModel, TagModel
from app.schemas.todo import TodoCreate, TodoUpdate, TodoPartialUpdate
from datetime import date, datetime
from app.repositories.tag import TagRepository

class TodoRepository:
    """Repository quản lý dữ liệu todo từ database"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, owner_id: int, todo_create: TodoCreate) -> TodoModel:
        """Tạo todo mới"""
        db_todo = TodoModel(
            title=todo_create.title,
            description=todo_create.description,
            is_done=todo_create.is_done,
            due_date=todo_create.due_date,
            owner_id=owner_id
        )
        self.db.add(db_todo)
        self.db.flush()  # Flush to get the ID
        
        # Add tags if provided
        if todo_create.tags:
            tag_repo = TagRepository(self.db)
            for tag_name in todo_create.tags:
                tag = tag_repo.get_or_create(tag_name)
                db_todo.tags.append(tag)
        
        self.db.commit()
        self.db.refresh(db_todo)
        return db_todo
    
    def get_all(
        self,
        owner_id: int,
        is_done: Optional[bool] = None,
        q: Optional[str] = None,
        sort: str = "created_at",
        limit: int = 10,
        offset: int = 0
    ) -> Tuple[list[TodoModel], int]:
        """Lấy danh sách todos của user (không bao gồm deleted)"""
        # Start with owner filter and NOT deleted filter
        query = self.db.query(TodoModel).filter(
            TodoModel.owner_id == owner_id,
            TodoModel.deleted_at == None  # Only non-deleted todos
        )
        
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
    
    def get_by_id(self, todo_id: int, owner_id: int) -> Optional[TodoModel]:
        """Lấy todo theo ID (check ownership, không bao gồm deleted)"""
        return self.db.query(TodoModel).filter(
            TodoModel.id == todo_id,
            TodoModel.owner_id == owner_id,
            TodoModel.deleted_at == None  # Only non-deleted
        ).first()
    
    def update(self, todo_id: int, owner_id: int, todo_update: TodoUpdate) -> Optional[TodoModel]:
        """Cập nhật todo (toàn bộ)"""
        db_todo = self.get_by_id(todo_id, owner_id)
        if db_todo:
            db_todo.title = todo_update.title
            db_todo.description = todo_update.description
            db_todo.is_done = todo_update.is_done
            db_todo.due_date = todo_update.due_date
            
            # Update tags
            if todo_update.tags is not None:
                db_todo.tags.clear()
                if todo_update.tags:
                    tag_repo = TagRepository(self.db)
                    for tag_name in todo_update.tags:
                        tag = tag_repo.get_or_create(tag_name)
                        db_todo.tags.append(tag)
            
            self.db.commit()
            self.db.refresh(db_todo)
        return db_todo
    
    def partial_update(self, todo_id: int, owner_id: int, todo_update: TodoPartialUpdate) -> Optional[TodoModel]:
        """Cập nhật một phần (PATCH)"""
        db_todo = self.get_by_id(todo_id, owner_id)
        if db_todo:
            if todo_update.title is not None:
                db_todo.title = todo_update.title
            if todo_update.description is not None:
                db_todo.description = todo_update.description
            if todo_update.is_done is not None:
                db_todo.is_done = todo_update.is_done
            if todo_update.due_date is not None:
                db_todo.due_date = todo_update.due_date
            
            # Update tags if provided
            if todo_update.tags is not None:
                db_todo.tags.clear()
                if todo_update.tags:
                    tag_repo = TagRepository(self.db)
                    for tag_name in todo_update.tags:
                        tag = tag_repo.get_or_create(tag_name)
                        db_todo.tags.append(tag)
            
            self.db.commit()
            self.db.refresh(db_todo)
        return db_todo
    
    def delete(self, todo_id: int, owner_id: int) -> Optional[TodoModel]:
        """Soft delete todo (đánh dấu deleted_at, không xóa dữ liệu)"""
        db_todo = self.get_by_id(todo_id, owner_id)
        if db_todo:
            db_todo.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(db_todo)
        return db_todo
    
    def restore(self, todo_id: int, owner_id: int) -> Optional[TodoModel]:
        """Restore deleted todo"""
        db_todo = self.db.query(TodoModel).filter(
            TodoModel.id == todo_id,
            TodoModel.owner_id == owner_id,
            TodoModel.deleted_at != None  # Only deleted todos
        ).first()
        if db_todo:
            db_todo.deleted_at = None
            self.db.commit()
            self.db.refresh(db_todo)
        return db_todo
    
    def permanent_delete(self, todo_id: int, owner_id: int) -> Optional[TodoModel]:
        """Xóa vĩnh viễn (thực sự xóa khỏi database)"""
        db_todo = self.db.query(TodoModel).filter(
            TodoModel.id == todo_id,
            TodoModel.owner_id == owner_id
        ).first()
        if db_todo:
            self.db.delete(db_todo)
            self.db.commit()
        return db_todo
    
    def get_overdue(self, owner_id: int, limit: int = 10, offset: int = 0) -> Tuple[list[TodoModel], int]:
        """Lấy todos quá hạn (không bao gồm deleted)"""
        today = date.today()
        query = self.db.query(TodoModel).filter(
            TodoModel.owner_id == owner_id,
            TodoModel.is_done == False,
            TodoModel.due_date < today,
            TodoModel.deleted_at == None  # Only non-deleted
        )
        total = query.count()
        items = query.order_by(TodoModel.due_date).offset(offset).limit(limit).all()
        return items, total
    
    def get_today(self, owner_id: int, limit: int = 10, offset: int = 0) -> Tuple[list[TodoModel], int]:
        """Lấy todos hôm nay (không bao gồm deleted)"""
        today = date.today()
        query = self.db.query(TodoModel).filter(
            TodoModel.owner_id == owner_id,
            TodoModel.is_done == False,
            TodoModel.due_date == today,
            TodoModel.deleted_at == None  # Only non-deleted
        )
        total = query.count()
        items = query.order_by(TodoModel.created_at).offset(offset).limit(limit).all()
        return items, total


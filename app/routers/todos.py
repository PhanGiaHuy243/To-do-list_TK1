from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.todo import (
    TodoCreate, TodoUpdate, TodoPartialUpdate, Todo, TodoListResponse
)
from app.services.todo import TodoService
from app.core.database import get_db

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)

@router.post("", response_model=Todo)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Tạo todo mới"""
    service = TodoService(db)
    return service.create_todo(todo)

@router.get("", response_model=TodoListResponse)
def get_todos(
    is_done: Optional[bool] = Query(None, description="Filter theo trạng thái"),
    q: Optional[str] = Query(None, description="Tìm kiếm theo title"),
    sort: Optional[str] = Query("created_at", description="Sort theo created_at hoặc -created_at"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Lấy danh sách todos với filter, search, sort, pagination"""
    service = TodoService(db)
    return service.get_todos(
        is_done=is_done,
        q=q,
        sort=sort,
        limit=limit,
        offset=offset
    )

@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết 1 todo"""
    service = TodoService(db)
    todo = service.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo không tìm thấy")
    return todo

@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """Cập nhật todo (toàn bộ)"""
    service = TodoService(db)
    todo = service.update_todo(todo_id, todo_update)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo không tìm thấy")
    return todo

@router.patch("/{todo_id}", response_model=Todo)
def partial_update_todo(
    todo_id: int, 
    todo_update: TodoPartialUpdate, 
    db: Session = Depends(get_db)
):
    """Cập nhật một phần todo (PATCH)"""
    service = TodoService(db)
    todo = service.partial_update_todo(todo_id, todo_update)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo không tìm thấy")
    return todo

@router.post("/{todo_id}/complete", response_model=Todo)
def complete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Đánh dấu todo là hoàn thành"""
    service = TodoService(db)
    todo = service.partial_update_todo(
        todo_id, 
        TodoPartialUpdate(is_done=True)
    )
    if not todo:
        raise HTTPException(status_code=404, detail="Todo không tìm thấy")
    return todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Xóa todo"""
    service = TodoService(db)
    todo = service.delete_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo không tìm thấy")
    return {"message": f"Đã xóa todo '{todo.title}'"}


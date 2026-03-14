from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class UserModel(Base):
    """SQLAlchemy model cho User"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationship
    todos = relationship("TodoModel", back_populates="owner")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


class TodoModel(Base):
    """SQLAlchemy model cho Todo"""
    
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_done = Column(Boolean, default=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationship
    owner = relationship("UserModel", back_populates="todos")
    
    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', owner_id={self.owner_id})>"

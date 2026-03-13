from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Tạo database URL (SQLite cho đơn giản)
DATABASE_URL = "sqlite:///./todolist.db"

# Tạo engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Tạo session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho models
Base = declarative_base()

def get_db():
    """Dependency để lấy DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

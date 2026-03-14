from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base
from app.core import models
from app.routers import todos, auth

# Tạo các bảng từ models
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# Health check endpoints
@app.get("/")
def read_root():
    return {"message": "Chào bạn! Đây là ứng dụng To-Do List"}

@app.get("/health")
def health_check():
    return {"status": "ok", "database": "connected"}

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(todos.router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

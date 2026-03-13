from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Cấu hình ứng dụng từ environment variables"""
    
    APP_NAME: str = "To-Do List API"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

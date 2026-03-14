from sqlalchemy.orm import Session
from app.core.models import TagModel

class TagRepository:
    """Repository cho Tag operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_name(self, name: str) -> TagModel | None:
        """Get tag by name"""
        return self.db.query(TagModel).filter(TagModel.name == name).first()
    
    def get_by_id(self, tag_id: int) -> TagModel | None:
        """Get tag by ID"""
        return self.db.query(TagModel).filter(TagModel.id == tag_id).first()
    
    def create(self, name: str) -> TagModel:
        """Create new tag"""
        tag = TagModel(name=name)
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag
    
    def get_or_create(self, name: str) -> TagModel:
        """Get tag by name or create if not exists"""
        tag = self.get_by_name(name)
        if not tag:
            tag = self.create(name)
        return tag
    
    def list_all(self) -> list[TagModel]:
        """Get all tags"""
        return self.db.query(TagModel).all()

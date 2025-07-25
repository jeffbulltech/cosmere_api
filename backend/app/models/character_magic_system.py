"""
CharacterMagicSystem junction table for many-to-many relationship between characters and magic systems.
"""
from sqlalchemy import Column, String, ForeignKey, Text, Boolean, Enum
from sqlalchemy.orm import relationship
import enum

from app.models.base import BaseModel


class MagicUserType(enum.Enum):
    """Magic user type enumeration."""
    PRACTITIONER = "practitioner"
    STUDENT = "student"
    FORMER = "former"
    POTENTIAL = "potential"
    UNKNOWN = "unknown"


class CharacterMagicSystem(BaseModel):
    """CharacterMagicSystem junction table representing character usage of magic systems."""
    
    __tablename__ = "character_magic_systems"
    
    id = Column(String(50), primary_key=True, index=True)
    character_id = Column(String(50), ForeignKey("characters.id"), nullable=False, index=True)
    magic_system_id = Column(String(50), ForeignKey("magic_systems.id"), nullable=False, index=True)
    user_type = Column(Enum(MagicUserType), default=MagicUserType.UNKNOWN)
    proficiency_level = Column(String(50), nullable=True)  # novice, intermediate, expert, master
    is_active = Column(Boolean, default=True)  # Is the character currently using this magic
    notes = Column(Text, nullable=True)  # Additional notes about the character's use of this magic
    
    # Relationships
    character = relationship("Character", back_populates="magic_systems")
    magic_system = relationship("MagicSystem", back_populates="users")
    
    def __repr__(self):
        return f"<CharacterMagicSystem(character_id='{self.character_id}', magic_system_id='{self.magic_system_id}')>"
    
    @classmethod
    def get_by_character(cls, db, character_id):
        """Get all magic systems used by a character."""
        return db.query(cls).filter(cls.character_id == character_id).all()
    
    @classmethod
    def get_by_magic_system(cls, db, magic_system_id):
        """Get all users of a magic system."""
        return db.query(cls).filter(cls.magic_system_id == magic_system_id).all()
    
    @classmethod
    def get_active_users(cls, db, magic_system_id):
        """Get active users of a magic system."""
        return db.query(cls).filter(
            cls.magic_system_id == magic_system_id,
            cls.is_active == True
        ).all()
    
    @classmethod
    def get_by_user_type(cls, db, character_id, user_type):
        """Get magic systems by user type for a character."""
        return db.query(cls).filter(
            cls.character_id == character_id,
            cls.user_type == user_type
        ).all() 
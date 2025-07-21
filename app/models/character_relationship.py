from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class CharacterRelationship(BaseModel):
    """CharacterRelationship model representing relationships between characters."""
    
    __tablename__ = "character_relationships"
    
    # Relationships
    character_id = Column(
        String(36),
        ForeignKey("characters.id"),
        nullable=False,
        index=True
    )
    related_character_id = Column(
        String(36),
        ForeignKey("characters.id"),
        nullable=False,
        index=True
    )
    book_context_id = Column(
        String(36),
        ForeignKey("books.id"),
        nullable=True,
        index=True
    )
    
    # Relationship details
    relationship_type = Column(String(100), nullable=False, index=True)  # friend, enemy, mentor, etc.
    description = Column(Text, nullable=True)
    
    # Relationships
    character = relationship(
        "Character",
        foreign_keys=[character_id],
        back_populates="relationships"
    )
    related_character = relationship(
        "Character",
        foreign_keys=[related_character_id],
        back_populates="related_characters"
    )
    book_context = relationship("Book")
    
    def __repr__(self):
        return f"<CharacterRelationship(character='{self.character.name if self.character else None}', related='{self.related_character.name if self.related_character else None}', type='{self.relationship_type}')>"
    
    @property
    def is_positive_relationship(self) -> bool:
        """Check if this is a positive relationship."""
        positive_types = ["friend", "mentor", "student", "ally", "family", "lover", "spouse"]
        return self.relationship_type.lower() in positive_types
    
    @property
    def is_negative_relationship(self) -> bool:
        """Check if this is a negative relationship."""
        negative_types = ["enemy", "rival", "nemesis", "betrayer", "traitor"]
        return self.relationship_type.lower() in negative_types
    
    @property
    def is_neutral_relationship(self) -> bool:
        """Check if this is a neutral relationship."""
        return not (self.is_positive_relationship or self.is_negative_relationship)
    
    def to_dict(self) -> dict:
        """Convert relationship to dictionary with additional computed fields."""
        base_dict = super().to_dict()
        base_dict.update({
            "is_positive_relationship": self.is_positive_relationship,
            "is_negative_relationship": self.is_negative_relationship,
            "is_neutral_relationship": self.is_neutral_relationship,
        })
        return base_dict
    
    @classmethod
    def get_by_character(cls, db, character_id: str):
        """Get all relationships for a specific character."""
        return db.query(cls).filter(
            (cls.character_id == character_id) |
            (cls.related_character_id == character_id)
        ).all()
    
    @classmethod
    def get_by_relationship_type(cls, db, relationship_type: str):
        """Get relationships by type."""
        return db.query(cls).filter(cls.relationship_type == relationship_type).all()
    
    @classmethod
    def get_positive_relationships(cls, db, character_id: str):
        """Get positive relationships for a character."""
        positive_types = ["friend", "mentor", "student", "ally", "family", "lover", "spouse"]
        return db.query(cls).filter(
            ((cls.character_id == character_id) | (cls.related_character_id == character_id)) &
            cls.relationship_type.in_(positive_types)
        ).all()
    
    @classmethod
    def get_negative_relationships(cls, db, character_id: str):
        """Get negative relationships for a character."""
        negative_types = ["enemy", "rival", "nemesis", "betrayer", "traitor"]
        return db.query(cls).filter(
            ((cls.character_id == character_id) | (cls.related_character_id == character_id)) &
            cls.relationship_type.in_(negative_types)
        ).all()
    
    @classmethod
    def get_by_book_context(cls, db, book_id: str):
        """Get relationships that have a specific book context."""
        return db.query(cls).filter(cls.book_context_id == book_id).all()
    
    @classmethod
    def get_between_characters(cls, db, character1_id: str, character2_id: str):
        """Get relationships between two specific characters."""
        return db.query(cls).filter(
            ((cls.character_id == character1_id) & (cls.related_character_id == character2_id)) |
            ((cls.character_id == character2_id) & (cls.related_character_id == character1_id))
        ).all() 
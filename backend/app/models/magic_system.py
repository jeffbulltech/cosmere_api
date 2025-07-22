from sqlalchemy import Column, String, Text
from app.core.database import Base

class MagicSystem(Base):
    __tablename__ = "magic_systems"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    universe = Column(String, nullable=True)
    related = Column(Text, nullable=True)
    description = Column(Text, nullable=True)

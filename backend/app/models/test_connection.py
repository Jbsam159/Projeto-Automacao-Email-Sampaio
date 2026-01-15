from sqlalchemy import Column, Integer, String
from app.core.database import Base

class TestConnection(Base):
    __tablename__ = "test_connection"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

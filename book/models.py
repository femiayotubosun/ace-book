from sqlalchemy import Column, String, Boolean, Integer
from common.database import Base


class Book(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    title = Column(
        String,
    )

    def __repr__(self) -> str:
        return f"{self.title}"

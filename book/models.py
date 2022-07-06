import uuid
from sqlalchemy import Column, ForeignKey, String, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from common.database import Base


class Book(Base):
    __tablename__ = "books"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(
        String,
    )

    description = Column(String)
    rating = Column(
        Integer,
        default=0,
    )
    chapters = relationship("Chapter", back_populates="book")

    def __repr__(self) -> str:
        return f"{self.title}"


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    title = Column(String)
    content = Column(Text)

    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"))
    book = relationship("Book", back_populates="chapters")

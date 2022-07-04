from email.policy import default
import uuid
from sqlalchemy import Column, String, Integer, null
from sqlalchemy.dialects.postgresql import UUID
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

    def __repr__(self) -> str:
        return f"{self.title}"

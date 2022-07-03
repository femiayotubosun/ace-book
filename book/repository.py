from contextlib import AbstractContextManager
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from .models import Book


class BooksRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[Book]:
        with self.session_factory as session:
            return session.query(Book).all()

    def get_by_id(self, book_id: int) -> Book:
        with self.session_factory as session:
            book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                raise Exception("Book not found")
                # raise BookNotFoundError(book_id)
            return book

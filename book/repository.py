from contextlib import AbstractContextManager
from typing import Callable, Iterator
from uuid import UUID
from requests import delete
from sqlalchemy.orm import Session
from book.schemas import CreateBook, UpdateBook
from .models import Book
from common.exceptions import NotFoundHTTPException


class BooksRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_many_books(self, q: str | None = None) -> Iterator[Book]:
        with self.session_factory() as session:
            if q:
                # FIXME
                return session.query(Book).filter(Book.title.ilike == q).all()
            return session.query(Book).all()

    def get_by_id(self, book_id: UUID) -> Book:
        with self.session_factory() as session:
            book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                raise NotFoundHTTPException(f"Book with ID: '{book_id}' was not found")
            return book

    def create_book(self, book_dto: CreateBook) -> Book:
        with self.session_factory() as session:
            book = Book()
            book.title = book_dto.title
            book.description = book_dto.description
            session.add(book)
            session.commit()
            session.refresh(book)
            return book

    def delete_book_by_id(self, book_id: UUID) -> None:
        with self.session_factory() as session:
            book: Book = self.get_by_id(book_id)
            session.delete(book)
            session.commit()

    def update_book_by_id(self, book_id: UUID, book_dto: UpdateBook) -> Book:
        with self.session_factory() as session:
            book: Book = session.query(Book).filter(Book.id == book_id).first()
            book.title = book_dto.title
            book.description = book_dto.description
            book.rating = book_dto.rating

            session.commit()
            session.refresh(book)

            return book

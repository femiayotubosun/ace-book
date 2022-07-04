from typing import Iterator
from uuid import UUID
from book.models import Book
from book.schemas import CreateBook, UpdateBook
from book.repository import BooksRepository


class BookService:
    def __init__(self, books_repository: BooksRepository) -> None:
        self._repository: BooksRepository = books_repository

    def get_many_books(self, q: str | None = None) -> Iterator[Book]:
        return self._repository.get_many_books(q)

    def get_one_book(self, book_id: UUID) -> Book:
        return self._repository.get_by_id(book_id)

    def create_book(self, book: CreateBook):
        return self._repository.create_book(book)

    def delete_book_by_id(self, book_id: UUID) -> None:
        return self._repository.delete_book_by_id(book_id)

    def update_book_by_id(self, book_id: UUID, book: UpdateBook) -> None:
        return self._repository.update_book_by_id(book_id, book)

from typing import Iterator
from book.models import Book
from book.repository import BooksRepository


class BookService:
    def __init__(self, books_repository: BooksRepository) -> None:
        self._repository: BooksRepository = books_repository

    def get_books(
        self,
    ) -> Iterator[Book]:
        return self._repository.get_all()

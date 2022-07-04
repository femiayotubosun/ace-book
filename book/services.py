from typing import Iterator
from book.models import Book
from book.repository import BooksRepository


class BookService:
    def __init__(self, books_repository: BooksRepository) -> None:
        self._repository: BooksRepository = books_repository

    def get_many_books(
        self,
    ) -> Iterator[Book]:
        return [
            Book(id=1, title="A Great Book"),
            Book(id=2, title="Anothe Great Book"),
        ]

from typing import Iterator
from uuid import UUID
from book.models import Book, Chapter
from book.repositories.chapter_repository import ChaptersRepository
from book.schemas import CreateBook, UpdateBook
from book.repositories.book_repository import BooksRepository
from book.schemas import CreateChapter


class BookService:
    def __init__(
        self, books_repository: BooksRepository, chapters_repository: ChaptersRepository
    ) -> None:
        self._repository: BooksRepository = books_repository
        self._chapters_repository: ChaptersRepository = chapters_repository

    def get_many_books(self, q: str | None = None) -> Iterator[Book]:
        return self._repository.get_many_books(q)

    def get_book_by_id(self, book_id: UUID) -> Book:
        return self._repository.get_book_by_id(book_id)

    def create_book(self, book: CreateBook):
        return self._repository.create_book(book)

    def delete_book_by_id(self, book_id: UUID) -> None:
        return self._repository.delete_book_by_id(book_id)

    def update_book_by_id(self, book_id: UUID, book: UpdateBook) -> None:
        return self._repository.update_book_by_id(book_id, book)

    def get_chapters_by_book_id(self, book_id: UUID) -> None:
        return self._chapters_repository.get_chapters_by_book_id(book_id)

    def get_chapter_by_id(self, chapter_id: UUID) -> Chapter:
        return self._chapters_repository.get_chapter_by_id(chapter_id)

    def create_chapter_for_book(self, book_id: UUID, chapter: CreateChapter):
        book = self.get_book_by_id(book_id)
        return self._chapters_repository.create_chapter_with_book(book)

    def delete_chapter_by_id(self, chapter_id: UUID):
        return self._chapters_repository.delete_chapter_by_id(chapter_id)

    def update_chapter_by_id(self, chapter_id: UUID, chapter: CreateChapter):
        return self._chapters_repository.update_chapter_by_id(chapter_id, chapter)

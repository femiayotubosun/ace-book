import pytest
from unittest import mock
from uuid import UUID, uuid4
from book.models import Book


from book.repositories.book_repository import BooksRepository
from book.repositories.chapter_repository import ChaptersRepository
from book.schemas import CreateBook, CreateChapter, UpdateBook
from book.services import BookService


class TestBookServices:
    def basic_book_assertions(self, data):
        assert "id" in data
        assert "title" in data
        assert "description" in data
        assert "rating" in data

    def get_uuid_string(self):
        return str(uuid4())

    def mocked_get_many_books_mocked_repo(q: str | None = None):
        return [q] if q else []

    def mocked_get_book_by_id_repo(book_id: UUID):
        return {
            "id": book_id,
            "title": "Test book",
            "description": "Test book description",
            "rating": 1,
        }

    def mocked_create_book(book: CreateBook):
        return {
            "id": str(uuid4()),
            "title": book["title"],
            "description": book["description"],
            "rating": 0,
        }

    def mocked_delete_book_by_id(book_id: UUID):
        return None

    def mocked_update_book_by_id(book_id: UUID, book: UpdateBook):
        return {
            "id": book_id,
            "title": book["title"],
            "description": book["description"],
            "rating": book["rating"],
        }

    def mocked_get_chapter_by_id(chapter_id: UUID):
        return {
            "id": chapter_id,
            "title": "Chapter 1",
            "content": "My stuff",
        }

    def mocked_get_chapters_by_book_id(book_id: UUID):
        return [
            {
                "id": uuid4(),
                "title": "Chapter 1",
                "content": "My stuff",
            },
            {
                "id": uuid4(),
                "title": "Chapter 2",
                "content": "My stuff",
            },
            {
                "id": uuid4(),
                "title": "Chapter 3",
                "content": "My stuff",
            },
        ]

    def mocked_update_chapter_by_id(chapter_id: UUID, chapter: CreateChapter):
        return {
            "id": str(chapter_id),
            "title": chapter["title"],
            "content": chapter["content"],
        }

    book_repository_mock: BooksRepository = mock.Mock(spec=BooksRepository)
    chapters_repository_mock: ChaptersRepository = mock.Mock(spec=ChaptersRepository)

    book_repository_mock.get_many_books.side_effect = mocked_get_many_books_mocked_repo
    book_repository_mock.get_book_by_id.side_effect = mocked_get_book_by_id_repo
    book_repository_mock.create_book.side_effect = mocked_create_book
    book_repository_mock.delete_book_by_id.side_effect = mocked_delete_book_by_id
    book_repository_mock.update_book_by_id.side_effect = mocked_update_book_by_id

    chapters_repository_mock.delete_chapter_by_id.return_value = None

    chapters_repository_mock.get_chapter_by_id.side_effect = mocked_get_chapter_by_id

    chapters_repository_mock.create_chapter_with_book.return_value = {
        "id": uuid4(),
        "title": "Chapter 1",
        "content": "My stuff",
    }
    chapters_repository_mock.get_chapters_by_book_id.side_effect = (
        mocked_get_chapters_by_book_id
    )

    chapters_repository_mock.update_chapter_by_id.side_effect = (
        mocked_update_chapter_by_id
    )

    book_service = BookService(book_repository_mock, chapters_repository_mock)

    def test_get_many_books_without_query(self):
        data = self.book_service.get_many_books()
        assert len(data) == 0
        assert type(data) == list

    def test_get_many_books_with_query(self):
        data = self.book_service.get_many_books("My stuff")
        assert len(data) == 1
        assert type(data) == list

    def test_get_book_by_id(self):
        data = self.book_service.get_book_by_id(uuid4())

        self.basic_book_assertions(data)

    def test_create_book(self):
        book: CreateBook = {"title": "Awesome", "description": "Book"}
        data = self.book_service.create_book(book)

        self.basic_book_assertions(data)

    def test_delete_book_by_id(self):
        data = self.book_service.delete_book_by_id(uuid4())

        assert data is None

    def test_update_book_by_id(self):
        book: UpdateBook = {"title": "Awesome", "description": "Book", "rating": 4}
        data = self.book_service.update_book_by_id(uuid4(), book)

        self.basic_book_assertions(data)

        assert book["title"] == data["title"]

    def test_get_chapter_by_id(self):
        data = self.book_service.get_chapter_by_id(uuid4())

        assert "id" in data
        assert "title" in data
        assert "content" in data

    def test_get_chapters_by_book_id(self):
        data = self.book_service.get_chapters_by_book_id(uuid4())

        assert type(data) == list
        assert len(data) == 3

    def test_create_chapter_for_book(self):
        data = self.book_service.create_chapter_for_book(
            uuid4(), {"title": "Chapter 1", "content": "Chapter content"}
        )

        assert "id" in data
        assert "title" in data
        assert "content" in data

    def test_delete_chapter_by_id(self):
        data = self.book_service.delete_chapter_by_id(uuid4())

        assert data is None

    def test_update_chapter_by_id(self):
        id = uuid4()
        data = self.book_service.update_chapter_by_id(
            id, {"title": "Stuff", "content": "More stuff"}
        )
        assert data["id"] == str(id)
        assert data["title"] == "Stuff"
        assert data["content"] == "More stuff"

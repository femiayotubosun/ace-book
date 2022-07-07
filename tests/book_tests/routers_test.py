import json
from unittest import mock
from urllib import response
from uuid import UUID, uuid4
import pytest
from fastapi.testclient import TestClient

from book.services import BookService
from book.models import Book
from book.schemas import CreateBook, CreateChapter, UpdateBook
from app import app


@pytest.fixture
def client():
    yield TestClient(app)


def basic_book_data_assertions(data: dict):
    assert "title" in data
    assert "description" in data
    assert "rating" in data
    assert "id" in data


class TestBookRouters:
    BOOK_TEST_DICT = {
        "id": uuid4(),
        "title": "A great book",
        "description": "A description",
        "rating": 0,
    }

    def get_uuid_string(self):
        return str(uuid4())

    def mocked_create_book_service(book: CreateBook):
        return {
            "id": uuid4(),
            "title": book.title,
            "description": book.description,
            "rating": 0,
        }

    def mocked_get_book_by_id_service(id: str):
        return {
            "id": id,
            "title": "A great book",
            "description": "A description",
            "rating": 0,
        }

    def mocked_update_book_by_id_service(id: str, book: UpdateBook):
        return {
            "id": id,
            "title": book.title,
            "description": book.description,
            "rating": book.rating,
        }

    def mocked_get_chapters_by_book_id(id: str):
        return []

    def mocked_create_chapter_for_book(book_id: UUID, chapter: CreateChapter):
        return {
            "id": uuid4(),
            "title": chapter.title,
            "content": chapter.content,
            "book_id": book_id,
        }

    service_mock = mock.Mock(spec=BookService)
    service_mock.get_many_books.return_value = [
        Book(id=1, title="A Great Book"),
        Book(id=2, title="Another Great Book"),
    ]
    service_mock.create_book.side_effect = mocked_create_book_service
    service_mock.get_book_by_id.side_effect = mocked_get_book_by_id_service
    service_mock.update_book_by_id.side_effect = mocked_update_book_by_id_service
    service_mock.get_chapters_by_book_id.return_value = mocked_get_chapters_by_book_id
    service_mock.create_chapter_for_book.side_effect = mocked_create_chapter_for_book
    service_mock.delete_book_by_id.return_value = None
    service_mock.delete_chapter_by_id.return_value = None
    service_mock.get_chapter_by_id.return_value = {
        "id": uuid4(),
        "title": "Chapter 1",
        "content": "My chapter contet",
    }

    def test_get_many_books(self, client):

        with app.container.book_service.override(self.service_mock):
            response = client.get("/books")

        assert response.status_code == 200
        data = response.json()

        assert data == [
            {"id": 1, "title": "A Great Book"},
            {"id": 2, "title": "Another Great Book"},
        ]

    def test_create_book(self, client):
        with app.container.book_service.override(self.service_mock):
            req_data: CreateBook = {
                "title": "A Great book",
                "description": "A Great description",
            }
            response = client.post("/books/", json=req_data)
            assert response.status_code == 201
            data = response.json()

            assert data["title"] == req_data["title"]
            assert data["description"] == req_data["description"]
            assert data["rating"] == 0
            assert type(data["id"]) == str

    def test_get_book_by_id(self, client):
        with app.container.book_service.override(self.service_mock):
            response = client.get(f"/books/b8277ce1-2f99-4fa9-a43f-ddf4e6078877/")

            data: dict = response.json()

            assert response.status_code == 200
            basic_book_data_assertions(data)

    def test_update_book_by_id(self, client):
        with app.container.book_service.override(self.service_mock):
            test_data = self.BOOK_TEST_DICT
            id = str(test_data["id"])
            del test_data["id"]

            response = client.put(f"/books/{id}", json=test_data)
            data = response.json()

            assert response.status_code == 200
            basic_book_data_assertions(data)

    def test_delete_book_by_id(self, client):
        with app.container.book_service.override(self.service_mock):
            id = self.get_uuid_string()

            response = client.delete(f"/books/{id}")
            data = response.json()

            assert response.status_code == 204
            assert data is None

    def test_get_chapters_by_book_id(self, client):
        with app.container.book_service.override(self.service_mock):

            id = self.get_uuid_string()

            response = client.get(f"/books/{id}/chapters/")
            data = response.json()

            assert response.status_code == 200
            # assert type(data) == list

    def test_create_chapter_by_book_id(self, client):
        with app.container.book_service.override(self.service_mock):
            id = self.get_uuid_string()
            test_chapter_data = {
                "title": "My Awesome title",
                "content": "My Wholesome content",
            }

            response = client.post(f"/books/{id}/chapters", json=test_chapter_data)

            assert response.status_code == 201

            data = response.json()

            assert "id" in data
            assert "title" in data
            assert "content" in data
            assert data["book_id"] == id

    def test_delete_chapter_by_id(self, client):
        with app.container.book_service.override(self.service_mock):
            id = self.get_uuid_string()

            response = client.delete(f"/chapters/{id}")
            data = response.json()

            assert response.status_code == 204

    def test_get_chapter_by_id(self, client):
        with app.container.book_service.override(self.service_mock):
            id = self.get_uuid_string()
            response = client.get(f"/chapters/{id}")
            data = response.json()

            assert response.status_code == 200
            assert "id" in data
            assert "title" in data
            assert "content" in data

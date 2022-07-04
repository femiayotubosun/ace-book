from unittest import mock
from urllib import response
import pytest
from fastapi.testclient import TestClient

from book.services import BookService
from book.models import Book
from app import app


@pytest.fixture
def client():
    yield TestClient(app)


class TestBookRouters:

    service_mock = mock.Mock(spec=BookService)
    service_mock.get_many_books.return_value = [
        Book(id=1, title="A Great Book"),
        Book(id=2, title="Another Great Book"),
    ]

    def test_get_many_books(self, client):

        with app.container.book_service.override(self.service_mock):
            response = client.get("/books")

        assert response.status_code == 200
        data = response.json()

        assert data == [
            {"id": 1, "title": "A Great Book"},
            {"id": 2, "title": "Another Great Book"},
        ]

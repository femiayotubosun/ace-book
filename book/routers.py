from uuid import UUID
from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide
from config.containers import Container
from .services import BookService
from .schemas import CreateBook, ResponseBook, UpdateBook


router = APIRouter(tags=["books"], prefix="/books")


@router.get("/")
@inject
def get_many_books(
    q: str | None = None,
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.get_many_books(q)


@router.post(
    "/",
)
@inject
def create_book(
    book: CreateBook,
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.create_book(book)


@router.get("/{book_id}")
@inject
def get_book_by_id(
    book_id: UUID, book_service: BookService = Depends(Provide[Container.book_service])
):
    return book_service.get_one_book(book_id)


@router.put("/{book_id}")
@inject
def update_book_by_id(
    book_id: UUID,
    book: UpdateBook,
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.update_book_by_id(book_id, book)


@router.delete("/{book_id}")
@inject
def delete_book_by_id(
    book_id: UUID, book_service: BookService = Depends(Provide[Container.book_service])
):
    return book_service.delete_book_by_id(book_id)

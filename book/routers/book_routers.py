from uuid import UUID
from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide
from config.containers import Container
from book.services import BookService
from book.schemas import CreateBook, CreateChapter, ResponseBook, UpdateBook


router = APIRouter(tags=["books"], prefix="/books")


@router.get("/")
@inject
def get_many_books(
    q: str | None = None,
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.get_many_books(q)


@router.post("/", status_code=status.HTTP_201_CREATED)
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
    return book_service.get_book_by_id(book_id)


@router.put("/{book_id}")
@inject
def update_book_by_id(
    book_id: UUID,
    book: UpdateBook,
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.update_book_by_id(book_id, book)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_book_by_id(
    book_id: UUID, book_service: BookService = Depends(Provide[Container.book_service])
):
    return book_service.delete_book_by_id(book_id)


@router.get("/{book_id}/chapters")
@inject
def get_chapters_by_book_id(
    book_id: UUID, book_service: BookService = Depends(Provide[Container.book_service])
):
    return book_service.get_chapters_by_book_id(book_id)


@router.post("/{book_id}/chapters", status_code=status.HTTP_201_CREATED)
@inject
def create_chapter_by_book_id(
    book_id: UUID,
    chapter: CreateChapter,
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.create_chapter_for_book(book_id, chapter)


# @router.delete("/c")

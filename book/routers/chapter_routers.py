from uuid import UUID
from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide
from config.containers import Container
from book.services import BookService


router = APIRouter(tags=["chapters"], prefix="/chapters")


@router.get("/{chapter_id}")
@inject
def get_chapter_by_id(
    chapter_id: UUID,
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.get_chapter_by_id(chapter_id)


@router.delete("/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_chapter_by_id(
    chapter_id: UUID,
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.delete_chapter_by_id(chapter_id)

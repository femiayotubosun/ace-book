import imp
from fastapi import APIRouter, Depends, Response, status
from dependency_injector.wiring import inject, Provide

from config.containers import Container
from .services import BookService


router = APIRouter(tags=["books"], prefix="/books")


@router.get("/")
@inject
def get_many_books(
    book_service: BookService = Depends(Provide[Container.book_service]),
):
    return book_service.get_books()

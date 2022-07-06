from contextlib import AbstractContextManager
from typing import Callable, Iterator
from uuid import UUID
from sqlalchemy.orm import Session
from book.schemas import CreateChapter
from book.models import Chapter, Book
from common.exceptions import NotFoundHTTPException


class ChaptersRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self.session_factory = session_factory

    def get_chapter_by_id(self, chapter_id: UUID) -> Chapter:
        with self.session_factory() as session:
            chapter = session.query(Chapter).filter(Chapter.id == chapter_id).first()
            if not chapter:
                raise NotFoundHTTPException(
                    f"Chapter with ID: '{chapter_id}' was not found"
                )
            return chapter

    def get_chapters_by_book_id(self, book_id: UUID) -> Iterator[Chapter]:
        with self.session_factory() as session:
            chapters = session.query(Chapter).filter(Chapter.book_id == book_id)

            return chapters

    def create_chapter_with_book(
        self, book: Book, chapter_dto: CreateChapter
    ) -> Chapter:
        with self.session_factory() as session:
            chapter = Chapter()
            chapter.book = book
            chapter.title = chapter_dto.title
            chapter.content = chapter_dto.content
            session.add(chapter)
            session.commit()
            session.refresh(chapter)
            return chapter

    def delete_chapter_by_id(self, chapter_id: UUID) -> None:
        with self.session_factory() as session:
            chapter: Chapter = self.get_chapter_by_id(chapter_id)
            session.delete(chapter)
            session.commit()

    def update_chapter_by_id(
        self, chapter_id: UUID, chapter_dto: CreateChapter
    ) -> Chapter:
        with self.session_factory() as session:
            chapter: Chapter = (
                session.query(Chapter).filter(Chapter.id == chapter_id).first()
            )
            chapter.title = chapter_dto.title
            chapter.content = chapter_dto.content

            session.commit()
            session.refresh(chapter)

            return chapter

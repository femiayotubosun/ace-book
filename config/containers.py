from dependency_injector import containers, providers
from dotenv import load_dotenv
from common.database import Database
from book.repositories.book_repository import BooksRepository
from book.repositories.chapter_repository import ChaptersRepository
from book.services import BookService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["book.routers.book_routers", "book.routers.chapter_routers"]
    )

    load_dotenv()

    config = providers.Configuration()
    config.db.url.from_env("DATABASE_URL")
    db = providers.Singleton(Database, db_url=config.db.url())

    book_repository = providers.Factory(
        BooksRepository, session_factory=db.provided.session
    )

    chapter_repository = providers.Factory(
        ChaptersRepository, session_factory=db.provided.session
    )

    book_service = providers.Factory(
        BookService,
        books_repository=book_repository,
        chapters_repository=chapter_repository,
    )

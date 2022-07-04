from dependency_injector import containers, providers
from dotenv import load_dotenv
from common.database import Database
from book.repository import BooksRepository
from book.services import BookService

import os


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["book.routers"])

    load_dotenv()
    print(f'dATABASE.URL{os.getenv("DATABASE_url")}')

    config = providers.Configuration()
    config.db.url.from_env("DATABASE_URL")
    db = providers.Singleton(Database, db_url=config.db.url())

    book_repository = providers.Factory(
        BooksRepository, session_factory=db.provided.session
    )
    book_service = providers.Factory(BookService, books_repository=book_repository)

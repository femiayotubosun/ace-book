from fastapi import FastAPI
from config.containers import Container
from book import routers as book_router


def create_app() -> FastAPI:
    container = Container()

    db = container.db()
    db.create_database()
    app = FastAPI()
    app.container = container
    # Add routes here
    app.include_router(book_router.router)

    return app


app = create_app()

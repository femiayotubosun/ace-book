from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.containers import Container
from book.routers.book_routers import router as book_router
from book.routers.chapter_routers import router as chapter_router


def create_app() -> FastAPI:
    container = Container()

    db = container.db()
    db.create_database()
    app = FastAPI()
    app.container = container

    # cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_headers=["*"],
        allow_methods=["GET", "POST", "PUT", "DELETE"],
    )

    # Add routes here
    app.include_router(book_router)
    app.include_router(chapter_router)

    return app


app = create_app()

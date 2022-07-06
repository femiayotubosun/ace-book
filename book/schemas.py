from uuid import UUID
from pydantic import BaseModel, Field


class ResponseBook(BaseModel):
    id: UUID
    title: str = Field(title="Title of the book", min_length=1, max_length=100)
    description: str | None = Field(
        title="Description of the book", min_length=1, max_length=200
    )
    rating: int = Field(gt=-1, lt=6)

    class Config:
        schema_extra = {
            "example": {
                "id": "8fd66002-9a2d-4849-9206-7ba18e051e18",
                "title": "An Awesome Book",
                "description": "An awesome Description",
                "rating": 3,
            }
        }


class CreateBook(BaseModel):
    title: str = Field(title="Title of the book", min_length=1, max_length=100)
    description: str | None = Field(
        title="Description of the book", min_length=1, max_length=200
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "An Awesome Book",
                "description": "An awesome Description",
            }
        }


class UpdateBook(BaseModel):
    title: str | None = Field(title="Title of the book", min_length=1, max_length=100)
    description: str | None = Field(
        title="Description of the book", min_length=1, max_length=200
    )
    rating: int = Field(gt=-1, lt=6)

    class Config:
        schema_extra = {
            "example": {
                "id": "8fd66002-9a2d-4849-9206-7ba18e051e18",
                "title": "An Awesome Book",
                "description": "An awesome Description",
                "rating": 3,
            }
        }


class CreateChapter(BaseModel):
    title: str = Field(title="Title of the chapter")
    content: str = Field(title="Content of the book", min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "title": "Chapter One",
                "content": "<i>He moved through the air</>",
            }
        }


class ResponseChapter(BaseModel):
    id: UUID
    title: str = Field(title="Title of the chapter")
    content: str = Field(title="Content of the book", min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "title": "Chapter One",
                "content": "<i>He moved through the air</>",
            }
        }

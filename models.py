from pydantic import BaseModel, Field
from typing import List, Optional


class Book(BaseModel):
    book_id: int
    title: str
    author: str
    description: Optional[str] = None
    rating: int
    review: str

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    rating: int
    review: str


class User(BaseModel):
    user_id: int
    username: str
    book_ids: List[int] = Field(default_factory=list)

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str


class UserBookUpdate(BaseModel):
    book_ids: List[int]

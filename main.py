from fastapi import FastAPI, Depends, HTTPException
from pymongo.database import Database
from typing import List

from database import get_db
from crud import (
    create_user,
    fetch_users,
    create_book,
    fetch_books,
    fetch_book,
    fetch_user_books,
    add_existing_book_to_user,
    update_user_book_list,
    delete_book,
    delete_user,
)
from models import (
    User,
    UserCreate,
    UserBookUpdate,
    Book,
    BookCreate,
)

app = FastAPI()

"""
User operations:
"""


@app.post("/users/", response_model=User)
def add_user(user: UserCreate, db: Database = Depends(get_db)):
    return create_user(db, user.username)


@app.get("/users/", response_model=List[User])
def list_users(db: Database = Depends(get_db)):
    return fetch_users(db)


@app.post("/users/{user_id}/books/{book_id}")
def add_book_to_user(user_id: int, book_id: int, db: Database = Depends(get_db)):
    success = add_existing_book_to_user(db, user_id, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")

    return {"status": "book added to user"}


@app.put("/users/{user_id}/books")
def update_user_books(
    user_id: int, payload: UserBookUpdate, db: Database = Depends(get_db)
):
    success = update_user_book_list(db, user_id, payload.book_ids)
    if not success:
        raise HTTPException(
            status_code=400, detail="User not found or invalid book IDs"
        )

    return {"status": "user book list updated"}


@app.get("/users/{user_id}/books", response_model=List[Book])
def get_user_books(user_id: int, db: Database = Depends(get_db)):
    return fetch_user_books(db, user_id)


"""
Book operations :

"""


@app.get("/books/", response_model=List[Book])
def list_books(db: Database = Depends(get_db)):
    return fetch_books(db)


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Database = Depends(get_db)):
    book = fetch_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books/", response_model=Book)
def add_book(book: BookCreate, db: Database = Depends(get_db)):
    return create_book(db, book.dict())


@app.delete("/books/{book_id}")
def delete_book_endpoint(book_id: int, db: Database = Depends(get_db)):
    success = delete_book(db, book_id)

    if not success:
        raise HTTPException(status_code=404, detail="Book not found")

    return {"status": "book deleted"}


@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Database = Depends(get_db)):
    success = delete_user(db, user_id)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"status": "user deleted"}

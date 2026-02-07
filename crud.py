from pymongo.database import Database
from database import (
    add_book,
    add_user,
    get_all_users,
    get_all_books,
    get_book_by_id,
    add_book_to_user,
    update_user_books,
    delete_book_by_id,
    delete_user_by_id,
    remove_book_from_all_users,
)


def create_user(db: Database, username: str):
    return add_user(db, {"username": username})


def fetch_users(db: Database):
    return get_all_users(db)


def add_existing_book_to_user(db: Database, user_id: int, book_id: int) -> bool:
    book = get_book_by_id(db, book_id)
    if not book:
        return False

    add_book_to_user(db, user_id, book_id)
    return True


def update_user_book_list(db: Database, user_id: int, book_ids: list[int]) -> bool:
    user = db["users"].find_one({"user_id": user_id})
    if not user:
        return False

    unique_ids = list(set(book_ids))
    existing = db["books"].count_documents({"book_id": {"$in": unique_ids}})
    if existing != len(unique_ids):
        return False

    update_user_books(db, user_id, unique_ids)
    return True


def fetch_user_books(db: Database, user_id: int):
    user = db["users"].find_one({"user_id": user_id})
    if not user:
        return []

    return list(
        db["books"].find({"book_id": {"$in": user.get("book_ids", [])}}, {"_id": 0})
    )


def create_book(db: Database, book_data: dict):
    return add_book(db, book_data)


def fetch_books(db: Database):
    return get_all_books(db)


def fetch_book(db: Database, book_id: int):
    return get_book_by_id(db, book_id)


def delete_book(db: Database, book_id: int) -> bool:
    result = delete_book_by_id(db, book_id)

    if result.deleted_count == 0:
        return False

    remove_book_from_all_users(db, book_id)
    return True


def delete_user(db: Database, user_id: int) -> bool:
    result = delete_user_by_id(db, user_id)
    return result.deleted_count > 0

import os
from pymongo import MongoClient, ReturnDocument
from pymongo.database import Database


MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI environment variable not set")

client = MongoClient(MONGO_URI)
db = client["book_organization"]


def get_db() -> Database:
    return db

 
def get_next_book_id(db: Database) -> int:
    counter = db["counters"].find_one_and_update(
        {"_id": "book_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return counter["seq"]


def get_next_user_id(db: Database) -> int:
    counter = db["counters"].find_one_and_update(
        {"_id": "user_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return counter["seq"]


def add_book(db: Database, book: dict):
    book["book_id"] = get_next_book_id(db)
    book["title_normalized"] = book["title"].casefold()
    db["books"].insert_one(book)
    return book


def get_all_books(db: Database):
    return list(db["books"].find({}, {"_id": 0}))


def get_book_by_id(db: Database, book_id: int):
    return db["books"].find_one({"book_id": book_id}, {"_id": 0})


def add_user(db: Database, user: dict):
    user["user_id"] = get_next_user_id(db)
    user["book_ids"] = []
    db["users"].insert_one(user)
    return user


def get_all_users(db: Database):
    return list(db["users"].find({}, {"_id": 0}))


def add_book_to_user(db: Database, user_id: int, book_id: int):
    return db["users"].update_one(
        {"user_id": user_id}, {"$addToSet": {"book_ids": book_id}}
    )


def update_user_books(db: Database, user_id: int, book_ids: list[int]):
    return db["users"].update_one(
        {"user_id": user_id}, {"$set": {"book_ids": book_ids}}
    )


def delete_book_by_id(db: Database, book_id: int):
    return db["books"].delete_one({"book_id": book_id})


def remove_book_from_all_users(db: Database, book_id: int):
    db["users"].update_many({}, {"$pull": {"book_ids": book_id}})


def delete_user_by_id(db: Database, user_id: int):
    return db["users"].delete_one({"user_id": user_id})

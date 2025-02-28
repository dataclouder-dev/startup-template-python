# from app.modules.mongo.mongo import db

from dataclouder_mongo.mongo import get_db

collection = "sources"


def save_source(source: dict) -> None:
    db = get_db()
    print(db)
    # db[collection].insert_one(source)

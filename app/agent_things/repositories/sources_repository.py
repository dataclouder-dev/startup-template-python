# from app.modules.mongo.mongo import db

from dataclouder_mongo.mongo import get_db

collection = "sources_llm"


def save_source(source: dict) -> None:
    db = get_db()
    print(db)


def get_resource(resource_id: str) -> dict:
    db = get_db()
    return db[collection].find_one({"type": "notion"})

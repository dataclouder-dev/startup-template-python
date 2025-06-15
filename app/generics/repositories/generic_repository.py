from bson import ObjectId
from dataclouder_core.models.models import FiltersConfig
from dataclouder_mongo.mongo import get_db

from app.generics.models.generic_model import GenericModel

col_name = "generics"

db = get_db()


def find_generics(generic_id: str) -> dict:
    """Get generic by id."""
    collection = db[col_name]
    return collection.find_one({"_id": ObjectId(generic_id)})


def find_filtered_generics(filters: FiltersConfig) -> list:
    """Get generics filtered."""
    print(filters)
    collection = db[col_name]
    return collection.find(filters.model_dump())


def save_generic(generic: GenericModel) -> GenericModel:
    """Save generic insert if not exists, or update if exists."""
    collection = db[col_name]

    # Convert the model to dict for manipulation
    generic_dict = generic.model_dump()

    if hasattr(generic, "id") and generic.id:
        # Update existing document
        query = {"_id": ObjectId(generic.id)}
        # Remove id from the update data
        generic_dict.pop("id", None)
    else:
        # Create new document
        query = {"_id": ObjectId()}

    result = collection.find_one_and_replace(query, generic_dict, upsert=True, return_document=True)
    result["_id"] = str(result["_id"])
    return result


def delete_generic(generic_id: str) -> dict:
    """Delete generic."""
    collection = db[col_name]
    collection.delete_one({"_id": ObjectId(generic_id)})
    return {"message": "Generic deleted"}

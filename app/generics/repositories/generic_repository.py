from bson import ObjectId
from dataclouder_core.models.models import FiltersConfig

from app.generics.models.generic_model import GenericModel
from app.modules.mongo.mongo import db

col_name = "generics"


def find_generics(id: str) -> dict:
    """Get words"""
    collection = db[col_name]
    result = collection.find_one({"_id": ObjectId(id)})

    return result


def find_filtered_generics(filters: FiltersConfig) -> list:
    """Get words"""
    print(filters)
    collection = db[col_name]
    result = collection.find(filters.model_dump())
    return result


def save_generic(generic: GenericModel) -> GenericModel:
    """Save generic insert if not exists, or update if exists"""
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


def delete_generic(id: str) -> GenericModel:
    """Delete generic"""
    collection = db[col_name]
    collection.delete_one({"_id": ObjectId(id)})
    return {"message": "Generic deleted"}

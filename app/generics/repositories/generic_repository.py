from bson import ObjectId
from dataclouder_mongo.mongo import get_db

from pydantic import BaseModel
from typing import Any, Optional, Union

# TODO: in the future i'll move this to dataclouder_mongo


class OperationDto(BaseModel):
    action: str
    query: Optional[dict] = None
    payload: Optional[Union[dict, list]] = None
    projection: Optional[dict] = None
    options: Optional[dict] = None


def convert_ids(data):
    """
    Recursively convert ObjectId to str in dictionaries and lists.
    """
    if isinstance(data, list):
        return [convert_ids(item) for item in data]
    if isinstance(data, dict):
        return {k: convert_ids(v) if k != "_id" else str(v) if isinstance(v, ObjectId) else convert_ids(v) for k, v in data.items()}
    if isinstance(data, ObjectId):
        return str(data)
    return data


def ensure_object_id(query):
    """
    Ensure that _id in the query is a bson ObjectId if it's a string.
    """
    if not isinstance(query, dict):
        return query
    
    if "_id" in query and isinstance(query["_id"], str) and ObjectId.is_valid(query["_id"]):
        query["_id"] = ObjectId(query["_id"])
    
    return query



def execute_operation(collection_name: str, operation: OperationDto) -> Any:
    """Execute a generic database operation."""
    collection = get_db()[collection_name]
    action = operation.action
    query = ensure_object_id(operation.query or {})
    payload = operation.payload
    projection = operation.projection
    options = operation.options or {}

    if action == "findOne":
        result = collection.find_one(query, projection, **options)
        return convert_ids(result)
    elif action == "find":
        results = list(collection.find(query, projection, **options))
        return convert_ids(results)
    elif action == "create":
        if isinstance(payload, list):
            result = collection.insert_many(payload)
            return {"inserted_ids": [str(id) for id in result.inserted_ids]}
        else:
            result = collection.insert_one(payload)
            return {"inserted_id": str(result.inserted_id)}
    elif action == "updateOne":
        result = collection.update_one(query, payload, **options)
        return {"matched_count": result.matched_count, "modified_count": result.modified_count}
    elif action == "updateMany":
        result = collection.update_many(query, payload, **options)
        return {"matched_count": result.matched_count, "modified_count": result.modified_count}
    elif action == "deleteOne":
        result = collection.delete_one(query, **options)
        return {"deleted_count": result.deleted_count}
    elif action == "deleteMany":
        # Blocked for now as per requirements
        raise ValueError(f"Blocked for now: {action}")
    elif action == "aggregate":
        if not isinstance(payload, list):
             raise ValueError("Payload for aggregate must be a list (pipeline)")
        results = list(collection.aggregate(payload))
        return convert_ids(results)
    elif action == "findOneAndReplace":
        result = collection.find_one_and_replace(query, payload, **options)
        return convert_ids(result)
    else:
        raise ValueError(f"Unsupported action: {action}")

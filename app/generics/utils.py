from bson import ObjectId

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

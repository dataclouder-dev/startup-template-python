import requests
import json

BASE_URL = "http://localhost:8000/api/generics/operation"

def test_create():
    print("Testing create...")
    payload = {
        "action": "create",
        "payload": {
            "name": "Test Generic",
            "description": "Created via generic operation",
            "type": "gen1",
            "image": {},
            "relation": {}
        }
    }
    response = requests.post(BASE_URL, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get("inserted_id")

def test_find_one(generic_id):
    print("\nTesting findOne...")
    payload = {
        "action": "findOne",
        "query": {"_id": generic_id}
    }
    # Note: verify if _id needs ObjectId conversion in repo or if it handles string. 
    # The repo uses generic_model.py which has fields. 
    # But for findOne with raw query, we might need to handle ObjectId conversion in repo 
    # if the user passes string ID but DB has ObjectId.
    # Let's see how it behaves. The repo code uses get_db()[col_name].find_one(query).
    # If I pass string, mongo might not find it if it expects ObjectId.
    # However, let's test.
    response = requests.post(BASE_URL, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_update_one(generic_id):
    print("\nTesting updateOne...")
    payload = {
        "action": "updateOne",
        "query": {"name": "Test Generic"}, # Using name for now to avoid ObjectId complexity in test for a moment
        "payload": {"$set": {"description": "Updated description"}}
    }
    response = requests.post(BASE_URL, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_delete_one(generic_id):
    print("\nTesting deleteOne...")
    payload = {
        "action": "deleteOne",
        "query": {"name": "Test Generic"}
    }
    response = requests.post(BASE_URL, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    # Ensure server is running before executing this
    try:
        id = test_create()
        if id:
             # For findOne with ID, we need to know if we should pass {"_id": ObjectId(id)} logic.
             # In raw JSON payload we can't pass ObjectId object.
             # The repo executes `collection.find_one(query)`.
             # If we want to find by ID, we likely need to handle ObjectId conversion 
             # on the client side if using pymongo directly, OR the repo needs to handle it.
             # But this is a "generic" operation, so it might expect raw queries.
             # Use a non-id query first for simplicity or handling strings.
             pass
        
        test_update_one(id)
        test_delete_one(id)
        
    except Exception as e:
        print(f"Error: {e}")

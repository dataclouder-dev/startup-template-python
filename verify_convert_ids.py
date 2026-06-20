from app.generics.utils import convert_ids
from bson import ObjectId

def test_convert_ids():
    oid1 = ObjectId()
    oid2 = ObjectId()
    
    # Test dictionary
    data = {
        "_id": oid1,
        "name": "test",
        "nested": {
            "id": oid2,
            "list": [oid1, oid2]
        }
    }
    
    converted = convert_ids(data)
    
    assert isinstance(converted["_id"], str)
    assert converted["_id"] == str(oid1)
    assert isinstance(converted["nested"]["id"], str)
    assert converted["nested"]["id"] == str(oid2)
    assert all(isinstance(x, str) for x in converted["nested"]["list"])
    assert converted["nested"]["list"] == [str(oid1), str(oid2)]
    
    # Test list
    data_list = [{"_id": oid1}, {"_id": oid2}]
    converted_list = convert_ids(data_list)
    assert all(isinstance(x["_id"], str) for x in converted_list)
    
    # Test single ObjectId
    assert convert_ids(oid1) == str(oid1)
    
    print("All tests passed!")

if __name__ == "__main__":
    test_convert_ids()

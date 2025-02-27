from fastapi import APIRouter

from app.modules.mongo import mongo

# from app.conversations import conversation_agents

router = APIRouter()


@router.get("/api/mongo/get_all_data_in_collection", tags=["Mongo"])
async def get_all_data_in_collection(collection: str) -> list[dict]:
    data = mongo.get_documents_by_query_projection(collection, {}, {})
    return data

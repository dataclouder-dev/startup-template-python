# from app.modules.mongo.mongo import db

from dataclouder_mongo import mongo

from app.agents.models.agent_sources_model import AgentSource

collection = "agent_sources"


def save_source(source: AgentSource, return_dict: bool = False) -> dict | AgentSource:
    response = mongo.save_document(collection, source.model_dump())
    if return_dict:
        return response["document"]
    else:
        return AgentSource(**response["document"])


def get_resource(resource_id: str) -> dict:
    return mongo.get_document(collection, {"type": "notion"})


def find_sources_by_video_platform_id(platform_id: str) -> list[dict]:
    db = mongo.get_db()
    result = list(db[collection].find({"video.idPlatform": platform_id}))
    return mongo.transform_object_id_to_string(result)

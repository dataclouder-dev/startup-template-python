from app.agents.models.agent_sources_model import AgentSource, SourceType
from app.agents.repositories import agent_sources_repository


def test_save_source() -> None:
    source = AgentSource(type=SourceType.NOTION)
    source = agent_sources_repository.save_source(source)
    print(source)

from app.agents.repositories import agent_sources_repository


def test_get_resource() -> None:
    resource = agent_sources_repository.get_resource("test_resource")
    print(resource)

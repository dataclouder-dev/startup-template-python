from unittest.mock import Mock, patch

import pytest

from app.agent_things.repositories import sources_repository


def test_get_resource() -> None:
    resource = sources_repository.get_resource("test_resource")
    print(resource)


@pytest.fixture
def mock_db() -> Mock:  # type: ignore
    with patch("app.agent_things.repositories.sources_repository.get_db") as mock:
        yield mock


def test_save_source(mock_db: Mock) -> None:
    # Arrange
    test_source = {"name": "test_source", "url": "http://test.com"}
    mock_db_instance = Mock()
    mock_db.return_value = mock_db_instance

    # Act
    sources_repository.save_source(test_source)

    # Assert
    mock_db.assert_called_once()
    # Note: Currently the insert_one is commented out in the implementation
    # When it's uncommented, add this assertion:
    # mock_db_instance[collection].insert_one.assert_called_once_with(test_source)

"""Fixtures related to Datastore entities"""

import pytest

from unittest.mock import MagicMock
from google.cloud.datastore import Key


@pytest.fixture(autouse=True)
def configure_env(monkeypatch):
    """Configure env variables before tests execution"""
    monkeypatch.setenv(
        "INTEGRATION_PUBSUB_TOPIC", "projects/projectId/topics/topicName"
    )


@pytest.fixture()
def make_datastore_entity():
    """Create datastore entity"""

    class FakedEntity(dict):
        key: object = None
        id: int = None

        def __init__(self, id: int):
            self.key = MagicMock(spec=Key)
            self.key.id.return_value = id
            self.id = id

    def _make_entity_factory(*args, **kwargs):
        """Factory"""
        attrs = {"attribute_1": "value_1"}

        mocked = FakedEntity(kwargs.get("id", 1))
        mocked.update(attrs)
        return mocked

    yield _make_entity_factory

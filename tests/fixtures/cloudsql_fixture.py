"""Fixtures related to Cloudsql """

import pytest
from abstractions.cloudsql import CloudSqlModel


@pytest.fixture()
def db():
    """"configure the sqlite db to pydal"""
    return CloudSqlModel('sqlite://db.sqlite3', True)


@pytest.fixture()
def mock_table(db):
    """"Mock table"""
    def _mock_table_with_item(*args, **kwargs):
        """Create item on table mock"""
        person = db.get_table("person", ["id", "name"])
        person.insert(id=kwargs.get("id", 1), name=kwargs.get("name", "test"))
        return person

    yield _mock_table_with_item

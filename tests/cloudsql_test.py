"""Tests for the CloudSqlModel"""
from pydal import Field
from pydal.objects import Table


def test_get_fields(db):
    """"Test"""
    fields = db.get_fields(["id", "name"])
    assert len(fields) == 2
    assert isinstance(fields, list)
    assert isinstance(fields[0], Field)


def test_get_table(db):
    """"Test"""
    person = db.get_table("person", ["id", "name"])
    assert isinstance(person, Table)


def test_filter_item(db, mock_table):
    """"Test"""
    mock_table()
    person = mock_table(**{"id": 2, "name": "test2"})
    result = db.session(person.id == 2).select()
    assert len(list(result)) == 1

from abstractions.datastore import Datastore
from unittest.mock import Mock
from google.cloud.datastore.entity import Entity
from unittest.mock import patch
import pytest


"""
#test_valid_information::ut
#test_with_invalid_information::ut
"""


@patch("google.cloud.datastore.Client")
def test_update_entity(mocked_datastore):
    """Test"""
    mocked_entity = Mock(spec=Entity)
    mocked_entity.key = Mock()
    Datastore().update_entity("kind", "namespace", mocked_entity, {})
    mocked_datastore.return_value.put.assert_called_once()


@patch("google.cloud.datastore.Client.__init__", return_value=None)
@patch("google.cloud.datastore.Client.key", return_value=None)
def test_get_entity(_1, _2, make_datastore_entity, mocker):
    """Test"""
    mocked_entity = make_datastore_entity()
    mocked_get = mocker.patch(
        "google.cloud.datastore.Client.get", return_value=mocked_entity
    )
    result = Datastore().get_entity("kind", "namespace", 1)
    mocked_get.assert_called_once()
    assert result is not None
    for key in mocked_entity.keys():
        assert result[key] == mocked_entity[key]
    assert result["id"] == mocked_entity.id


@patch("google.cloud.datastore.Client")
def test_get_entity_not_passing_id_should_raise_error(_):
    """Test"""
    with pytest.raises(ValueError):
        Datastore().get_entity(None, None, None)


@patch("google.cloud.datastore.Client.__init__", return_value=None)
@patch("google.cloud.datastore.Client.get", return_value=None)
@patch("google.cloud.datastore.Client.key", return_value=None)
def test_get_entity_not_existing_entity_should_raise_error(_1, _2, _3):
    """Test"""
    with pytest.raises(Exception):
        Datastore().get_entity("kind", "namespace", 1)


@patch("google.cloud.datastore.Client")
def test_query_entity_with_filters_passing_empty_list(mocked_datastore):
    Datastore().query_entity_with_filters("kind", "namespace", [])
    mocked_datastore.return_value.query.assert_called_once()


@patch("google.cloud.datastore.Client")
def test_query_entity_with_filters_passing_filters(mocked_datastore):
    filter_list = [["field1", ">=", "field2"]]
    Datastore().query_entity_with_filters("kind", "namespace", filter_list)
    mocked_datastore.return_value.query.assert_called_once()


@patch("google.cloud.datastore.Client")
def test_save_entity(mocked_datastore):
    Datastore().save_entity("kind", "namespace", {"data": "test"})
    mocked_datastore.return_value.put.assert_called_once()

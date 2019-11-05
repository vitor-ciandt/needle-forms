from abstractions.bigquery import BigQuery
from unittest.mock import patch
import pytest


"""
#test_valid_information::ut
#test_with_invalid_information::ut
"""


@pytest.mark.parametrize("field,value,operator,result",
                         [("source", "test", "=", "source='test'"),
                          ("source", 1, "=", "source=1")])
def test_get_operator(field, value, operator, result):
    """Test"""
    query = BigQuery().get_filter_with_operator(field, value, operator)
    assert query == result


@pytest.mark.parametrize("value,result",
                         [({"source": "test"}, "source='test'"),
                          ({"id": 1, "source": "test"},
                           "id=1, source='test'"),
                          ({}, "")])
def test_get_values(value, result):
    """Test"""
    query = BigQuery().get_values(value)
    assert query == result


@pytest.mark.parametrize("filters,result",
                         [([{"field": "source", "value": "test",
                             "operator": "="}], "WHERE source='test'"),
                          ([{"field": "source", "value": "test",
                             "operator": "="},
                            {"field": "id", "value": 1,
                             "operator": "="}],
                           "WHERE source='test' AND id=1"),
                          ([], "")])
def test_get_filters(filters, result):
    """Test"""
    query = BigQuery().get_filters(filters)
    assert query == result


@patch("google.cloud.bigquery.Client.query", return_value=[])
def test_update(mocked_bigquery):
    """Test"""
    errors = BigQuery().update("dataset", "table", {"id": 1},
                               [{"field": "test", "operator": "=",
                                 "value": "value"}])
    update_str = "UPDATE dataset.table SET id=1 WHERE test='value'"
    mocked_bigquery.assert_called_with(update_str)
    assert not errors


@patch("google.cloud.bigquery.Client.query", return_value=[])
def test_update_error_value(_):
    """Test"""
    with pytest.raises(ValueError):
        BigQuery().update("dataset", "table", {},
                          [{"field": "test", "operator": "=",
                            "value": "test"}])
    with pytest.raises(Exception):
        BigQuery().update("", "table", {"id": 1},
                          [{"field": "test", "operator": "=",
                            "value": "test"}])


@patch("google.cloud.bigquery.Client.query", return_value=[1])
def test_update_error_bigquery(_):
    """Test"""
    with pytest.raises(Exception):
        BigQuery().update("dataset", "table", {"id": 1},
                          [{"field": "test", "operator": "=",
                            "value": "test"}])
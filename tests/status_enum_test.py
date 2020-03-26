"""Tests for the StatusEnum class"""
from enums.status_enum import StatusEnum


def test_status_enum():
    """Test"""
    for status in StatusEnum:
        assert status.value in range(1, 5)

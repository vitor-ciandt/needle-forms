"""Tests for Pubsub class"""

from abstractions.pubsub import Pubsub
import pytest
from unittest.mock import patch


"""
#test_valid_information::ut
#test_with_invalid_information::ut
"""


def test_validate_topic_name():
    """Test"""

    with pytest.raises(ValueError):
        Pubsub.validate_topic_name("")

    with pytest.raises(ValueError):
        Pubsub.validate_topic_name("projects/projectId")

    with pytest.raises(ValueError):
        Pubsub.validate_topic_name("projects/projectId/topics/")

    Pubsub.validate_topic_name("projects/projectId/topics/topicName")


@patch("google.cloud.pubsub_v1.PublisherClient")
def test_publish_message(mocked_publisher):
    """Test"""
    pubsub = Pubsub()
    pubsub.publish_message("projects/projectId/topics/topicName", "Testing...")
    mocked_publisher.return_value.publish.assert_called_once()


@patch("google.cloud.pubsub_v1.PublisherClient")
def test_publish_message_with_empty_message_should_do_nothing(
    mocked_publisher
):
    """Test"""
    pubsub = Pubsub()
    pubsub.publish_message("projects/projectId/topics/topicName", "")
    mocked_publisher.return_value.publish.assert_not_called()

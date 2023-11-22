import pytest
from unittest.mock import MagicMock
from ingestion.kinesis_consumer import KinesisConsumer

def test_initialize_kinesis_client():
    consumer = KinesisConsumer("stream_name", "access_key", "secret_key", "region")
    consumer.initialize_kinesis_client = MagicMock()
    consumer.initialize_kinesis_client()
    consumer.initialize_kinesis_client.assert_called_once()
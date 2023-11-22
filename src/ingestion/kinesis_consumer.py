import json
import boto3
from botocore.exceptions import NoCredentialsError
from src.processing.data_processing import DataProcessing
from src.processing.analytics_models import DiagnosticAnalytics

class KinesisConsumer:
    def __init__(self, stream_name, aws_access_key, aws_secret_key, region_name):
        self.stream_name = stream_name
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.region_name = region_name
        self.kinesis_client = self.initialize_kinesis_client()
        self.data_processor = DataProcessing()
        self.analytics_model = DiagnosticAnalytics()

    def initialize_kinesis_client(self):
        return boto3.client(
            'kinesis',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.region_name
        )

    def start_consuming(self):
        try:
            response = self.kinesis_client.describe_stream(StreamName=self.stream_name)
            shard_id = response['StreamDescriptigiton']['Shards'][0]['ShardId']

            shard_iterator = self.kinesis_client.get_shard_iterator(
                StreamName=self.stream_name,
                ShardId=shard_id,
                ShardIteratorType='TRIM_HORIZON'
            )['ShardIterator']

            while True:
                records_response = self.kinesis_client.get_records(ShardIterator=shard_iterator, Limit=10)

                for record in records_response['Records']:
                    data_point = json.loads(record['Data'])
                    processed_data = self.data_processor.run_processing_pipeline([data_point])
                    insights = self.analytics_model.identify_factors_for_sales(processed_data)

                    # TODO: Add logic to handle the insights (e.g., store in a database, send alerts, etc.)
                    print("Processed Data:", processed_data)
                    print("Insights:", insights)

                shard_iterator = records_response['NextShardIterator']

        except NoCredentialsError as e:
            print(f"Error: {e} - Ensure AWS credentials are configured correctly.")

if __name__ == "__main__":
    stream_name = "kinesis_stream"
    access_key = "aws_access_key"
    secret_key = "aws_secret_key"
    region = "aws_region"

    consumer = KinesisConsumer(stream_name, access_key, secret_key, region)
    consumer.start_consuming()
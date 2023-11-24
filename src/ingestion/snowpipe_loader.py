import snowflake.connector
import boto3

SNOWFLAKE_ACCOUNT = 'snowflake_account_url'
SNOWFLAKE_USER = 'snowflake_username'
SNOWFLAKE_PASSWORD = 'snowflake_password'
SNOWFLAKE_DATABASE = 'snowflake_database'
SNOWFLAKE_WAREHOUSE = 'snowflake_warehouse'
SNOWFLAKE_SCHEMA = 'snowflake_schema'

AWS_ACCESS_KEY = 'aws_access_key'
AWS_SECRET_KEY = 'aws_secret_key'
KINESIS_STREAM_NAME = 'kinesis_stream_name'

con = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA
)

with con.cursor() as cur:
    cur.execute(f"CREATE OR REPLACE STAGE kinesis_stage")

kinesis_client = boto3.client(
    'kinesis',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='your_aws_region'
)

def load_data_into_snowflake(records):
    with con.cursor() as cur:
        for record in records:
            data = record['Data']
            cur.execute(f"INSERT INTO your_snowflake_table VALUES (%s)", (data,))

def main():
    response = kinesis_client.describe_stream(StreamName=KINESIS_STREAM_NAME)
    shard_id = response['StreamDescription']['Shards'][0]['ShardId']

    shard_iterator = kinesis_client.get_shard_iterator(
        StreamName=KINESIS_STREAM_NAME,
        ShardId=shard_id,
        ShardIteratorType='LATEST'
    )['ShardIterator']

    records = kinesis_client.get_records(ShardIterator=shard_iterator)['Records']

    load_data_into_snowflake(records)

if __name__ == "__main__":
    main()

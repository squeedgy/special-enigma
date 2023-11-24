import snowflake.connector
import boto3
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

SNOWFLAKE_USER = config['snowflake']['user']
SNOWFLAKE_PASSWORD = config['snowflake']['password']
SNOWFLAKE_ACCOUNT = config['snowflake']['account']
SNOWFLAKE_DATABASE = config['snowflake']['database']
SNOWFLAKE_WAREHOUSE = config['snowflake']['warehouse']
SNOWFLAKE_SCHEMA = config['snowflake']['schema']

AWS_ACCESS_KEY = config['aws']['access_key']
AWS_SECRET_KEY = config['aws']['secret_key']
KINESIS_STREAM_NAME = config['aws']['kinesis_stream_name']

con = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA
)

with con.cursor() as cur:
    cur.execute("CREATE OR REPLACE STAGE kinesis_stage")

kinesis_client = boto3.client(
    'kinesis',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name='aws_region'
)

def load_data_into_snowflake(records):
    with con.cursor() as cur:
        for record in records:
            data = record['Data']
            cur.execute(f"INSERT INTO snowflake_table VALUES (%s)", (data,))

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

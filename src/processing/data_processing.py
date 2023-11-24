import snowflake.connector
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

SNOWFLAKE_USER = config['snowflake']['user']
SNOWFLAKE_PASSWORD = config['snowflake']['password']
SNOWFLAKE_ACCOUNT = config['snowflake']['account']
SNOWFLAKE_DATABASE = config['snowflake']['database']
SNOWFLAKE_WAREHOUSE = config['snowflake']['warehouse']
SNOWFLAKE_SCHEMA = config['snowflake']['schema']

con = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA
)

def data_processing_workflow():
    with con.cursor() as cur:
        cur.execute("""
            UPDATE streaming_table
            SET column1 = COALESCE(column1, 'default_value')
            WHERE column1 IS NULL
        """)

        cur.execute("""
            UPDATE streaming_table
            SET column2 = UPPER(column2)
        """)

        cur.execute("""
            UPDATE streaming_table t1
            SET column3 = t2.additional_info
            FROM reference_table t2
            WHERE t1.join_key = t2.join_key
        """)

if __name__ == "__main__":
    data_processing_workflow()

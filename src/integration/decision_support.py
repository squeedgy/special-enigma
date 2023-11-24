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

def query_real_time_data():
    with con.cursor() as cur:
        cur.execute("SELECT * FROM real_time_data_table;")
        result = cur.fetchall()
    return result

def transfer_data_to_analytics_tool(data):
    # TODO:
    pass

if __name__ == "__main__":
    real_time_data = query_real_time_data()
    transfer_data_to_analytics_tool(real_time_data)

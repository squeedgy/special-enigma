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

from alerting_system import send_alert_email

def check_pipeline_health():
    try:
        with con.cursor() as cur:
            cur.execute("SELECT 1")
            result = cur.fetchone()
            if result[0] != 1:
                raise Exception("Snowflake connection issue")

        with con.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM monitoring_table")
            metric_value = cur.fetchone()[0]
            if metric_value < threshold:
                raise Exception("Pipeline health metric below threshold")
        print("Pipeline is healthy")

    except Exception as e:
        send_alert_email("Pipeline Health Check Failed", f"Exception: {str(e)}")

def handle_exception(exception):
    with open('error_log.txt', 'a') as f:
        f.write(f"Exception: {str(exception)}\n")

def log_exception(exception):
    with open('error_log.txt', 'a') as f:
        f.write(f"Exception: {str(exception)}\n")

if __name__ == "__main__":
    check_pipeline_health()

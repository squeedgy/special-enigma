import snowflake.connector
import configparser

def check_security_settings():
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

    with con.cursor() as cur:
        cur.execute("SHOW PARAMETERS LIKE 'CLIENT_SESSION_KEEP_ALIVE'")
        result = cur.fetchone()
        print(f"Encryption for data in transit: {result[1]}")

        cur.execute("SHOW PARAMETERS LIKE 'DATA_ENCRYPTION_TYPE'")
        result = cur.fetchone()
        print(f"Encryption for data at rest: {result[1]}")

        cur.execute("SHOW PARAMETERS LIKE 'SECURE_PARAMETER'")
        result = cur.fetchone()
        print(f"Multi-Factor Authentication (MFA): {result[1]}")

if __name__ == "__main__":
    check_security_settings()

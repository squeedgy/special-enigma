import snowflake.connector
import json

def check_performance_settings():
    with open('snowflake_config.json', 'r') as config_file:
        snowflake_config = json.load(config_file)

    con = snowflake.connector.connect(
        user=snowflake_config['user'],
        password=snowflake_config['password'],
        account=snowflake_config['account'],
        warehouse=snowflake_config['warehouse'],
        database=snowflake_config['database'],
        schema=snowflake_config['schema']
    )

    with con.cursor() as cur:
        cur.execute("SHOW PARAMETERS LIKE 'WAREHOUSE_SIZE'")
        result = cur.fetchone()
        print(f"Warehouse size: {result[1]}")

        cur.execute("SHOW PARAMETERS LIKE 'CONCURRENCY_SCALING_POLICY'")
        result = cur.fetchone()
        print(f"Concurrency scaling policy: {result[1]}")

if __name__ == "__main__":
    check_performance_settings()

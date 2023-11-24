import snowflake.connector

def execute_sql_commands(sql_commands):
    SNOWFLAKE_USER = 'snowflake_username'
    SNOWFLAKE_PASSWORD = 'snowflake_password'
    SNOWFLAKE_ACCOUNT = 'snowflake_account_url'
    SNOWFLAKE_DATABASE = 'snowflake_database'
    SNOWFLAKE_WAREHOUSE = 'snowflake_warehouse'
    SNOWFLAKE_SCHEMA = 'snowflake_schema'

    con = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )

    with con.cursor() as cur:
        for sql_command in sql_commands:
            cur.execute(sql_command)

if __name__ == "__main__":
    optimization_commands = [
        "CREATE OR REPLACE TABLE table CLUSTER BY (cluster_column);",
        "CREATE INDEX idx_table_column ON table(column);",
        "ALTER TABLE table MODIFY COLUMN column1 VARCHAR(255);"
    ]

    execute_sql_commands(optimization_commands)

Before setting up the real-time analytics pipeline, ensure that you have the following prerequisites:

- Snowflake account credentials (username, password, account URL).
- AWS Kinesis stream set up with the stream name.
- Python installed on your system.

1. Clone the repository to your local machine

2. Configuration - Configure the pipeline by updating the config.ini file with your Snowflake account and AWS Kinesis stream details

config.ini
```
[snowflake]
user = snowflake_username
password = snowflake_password
account = snowflake_account_url
database = snowflake_database
warehouse = snowflake_warehouse
schema = snowflake_schema

[aws]
access_key = aws_access_key
secret_key = aws_secret_key
kinesis_stream_name = kinesis_stream_name

[email]
host = your_email_host
port = your_email_port
user = your_email_user
password = your_email_password
recipient = your_recipient_email
```


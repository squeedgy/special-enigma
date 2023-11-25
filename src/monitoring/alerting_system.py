import snowflake.connector
import configparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

config = configparser.ConfigParser()
config.read('config.ini')

SNOWFLAKE_USER = config['snowflake']['user']
SNOWFLAKE_PASSWORD = config['snowflake']['password']
SNOWFLAKE_ACCOUNT = config['snowflake']['account']
SNOWFLAKE_DATABASE = config['snowflake']['database']
SNOWFLAKE_WAREHOUSE = config['snowflake']['warehouse']
SNOWFLAKE_SCHEMA = config['snowflake']['schema']

EMAIL_HOST = config['email']['host']
EMAIL_PORT = config['email']['port']
EMAIL_USER = config['email']['user']
EMAIL_PASSWORD = config['email']['password']
RECIPIENT_EMAIL = config['email']['recipient']

con = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA
)

logging.basicConfig(filename='alerting_system.log', level=logging.ERROR)

def send_alert_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, RECIPIENT_EMAIL, msg.as_string())

        print("Alert email sent successfully")

    except Exception as e:
        logging.error(f"Error sending alert email: {str(e)}")

def configure_alerts():
    try:
        with con.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM alert_metric_table")
            alert_metric_value = cur.fetchone()[0]

            alert_threshold = alert_threshold

            if alert_metric_value > alert_threshold:
                send_alert_email("Alert: Metric Exceeded Threshold", f"Metric Value: {alert_metric_value}")
    
    except Exception as e:
        logging.error(f"Error configuring alerts: {str(e)}")

if __name__ == "__main__":
    configure_alerts()

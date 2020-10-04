import os
import yaml
import mysql.connector

# Load credentials.yaml file
CURR_DIR = os.path.abspath(os.path.dirname(__file__))
CREDENTIALS_YAML = os.path.join(CURR_DIR, '../credentials.yaml')
file_credentails = open(CREDENTIALS_YAML)
CREDENTIALS = yaml.load(file_credentails, Loader=yaml.FullLoader)

# Define variables
scope = CREDENTIALS['SCOPE']
credential_json_path = os.path.join(CURR_DIR, 'iff_gsheets_config.json')
source = CREDENTIALS['SOURCE']
DB_USER = CREDENTIALS['MYSQL_USERNAME']
DB_PASSWORD = CREDENTIALS['MYSQL_PASSWORD']
ACCEPT_MESSAGE = CREDENTIALS['ACCEPT_MESSAGE']
REJECT_MESSAGE = CREDENTIALS['REJECT_MESSAGE']
SUBMIT_MESSAGE = CREDENTIALS['SUBMIT_MESSAGE']

# Setup Connection
def connection():
    conn = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

conn = connection()

import mysql.connector

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credential_json_path = 'datakind.json'
source = 'Datakind -IFF dashboard'

DB_USER = 'datakind'
DB_PASSWORD = 'Datakind@123'
ACCEPT_MESSAGE = 'Accepted'
REJECT_MESSAGE = 'Rejected'
SUBMIT_MESSAGE = 'Submit'


def connection():
    conn = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD
    )

    return conn


conn = connection()

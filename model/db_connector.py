"""DB connector for accesing database"""
import os
from json import load
from mysql import connector

def connection():
    """
    Makes the connection to DB and returns the connection object.

    Returns:
        {mysql connector} -- MYSQL connector object
    """

    conn = connector.connect (
        host = os.environ.get('MYSQL_HOST'),
        user = os.environ.get('MYSQL_USERNAME'),
        password = os.environ.get('MYSQL_PASSWORD')
    )

    return conn

def execute_select_query(query:str):
    """
    Executes the SELECT query on MYSQL database

    Arguments:
        query {str} -- Query to execute
    Returns:
        {list} -- Columns returned by the query
        {list} -- Data returned by the query
    """

    conn = connection()

    cursor = conn.cursor()
    cursor.execute(query)

    # Get all the columns of data
    headers = [x[0] for x in cursor.description]
    data = cursor.fetchall()
    conn.close()

    return headers, data

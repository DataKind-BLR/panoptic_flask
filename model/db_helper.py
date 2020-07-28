"""DB connector for accesing database"""
import os
from json import load
from mysql import connector

def execute_select_query(query:str):
    """
    Executes the SELECT query on MYSQL database

    Arguments:
        query {str} -- Query to execute
    Returns:
        {list} -- Columns returned by the query
        {list} -- List of data returned by the query
    """

    conn = connector.connect (
        host = os.environ.get('MYSQL_HOST'),
        user = os.environ.get('MYSQL_USERNAME'),
        password = os.environ.get('MYSQL_PASSWORD')
    )

    cursor = conn.cursor()
    cursor.execute(query)

    # Get all the columns of data
    headers = [x[0] for x in cursor.description]
    data = cursor.fetchall()

    conn.close()

    return headers, data

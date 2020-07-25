"""DB connector for accesing database"""
from json import load
from mysql import connector

def connection(path_to_config=None):
    """
    Makes the connection to DB and returns the connection object.

    Arguments:
        path_to_config {str} -- Path to the config file which contatins credentials
    Returns:
        {mysql connector} -- MYSQL connector object
    """

    if not path_to_config:
        path_to_config = 'model/config.json'

    fp = open(path_to_config)
    config = load(fp)
    fp.close()

    conn = connector.connect (
        host = config['host'],
        user = config['user'],
        password = config['password']
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

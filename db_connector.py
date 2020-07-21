from json import load
from mysql import connector

def connection(path_to_config=None):
    """
    Makes the connection to DB and returns the connection object.
    """

    if not path_to_config:
        path_to_config = 'config.json'

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

    conn = connection()

    cursor = conn.cursor()
    cursor.execute(query)

    # Get all the columns of data
    headers = [x[0] for x in cursor.description]
    data = cursor.fetchall()
    conn.close()

    return headers, data
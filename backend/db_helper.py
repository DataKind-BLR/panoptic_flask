"""DB connector for accesing database"""    
import os
import yaml
from mysql import connector

CURR_DIR = os.path.abspath(os.path.dirname(__file__))
CREDENTIALS_YAML = os.path.join(CURR_DIR, '../credentials.yaml')

file_credentails = open(CREDENTIALS_YAML)
CREDENTIALS = yaml.load(file_credentails, Loader=yaml.FullLoader)


def execute_select_query(query, cache_filename=None):
    '''
    Executes the SELECT query on MYSQL database

    Arguments:
        query {str} -- Query to execute
        cache_filname {str} -- Cache filename for the respective Query
    Returns:
        {list} -- Columns returned by the query
        {list} -- List of data returned by the query
    '''
    conn = connector.connect(
        host=CREDENTIALS['MYSQL_HOST'],
        user=CREDENTIALS['MYSQL_USERNAME'],
        password=CREDENTIALS['MYSQL_PASSWORD'],
        database=CREDENTIALS['MYSQL_DATABASE']
    )
    cursor = conn.cursor()
    cursor.execute(query)

    # Get all the columns of data
    headers = [x[0] for x in cursor.description]
    data = cursor.fetchall()

    cursor.close()

    return headers, data

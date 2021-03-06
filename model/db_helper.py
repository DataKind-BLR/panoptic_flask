"""DB connector for accesing database"""	
import os
import time
import yaml
import pickle
from mysql import connector

# 20 minutes cache age
MAX_CACHE_AGE = 60*20

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

    """
    Read this: https://stackoverflow.com/questions/307438/how-can-i-tell-when-a-mysql-table-was-last-updated
    and this:  https://stackoverflow.com/questions/15749719/caching-mysql-query-returned-by-python-script
    """

    file_last_updated = time.time()
    regen = True
    """
    try:
        with open(cache_filename, 'r') as cache:
            cached = pickle.load(cache)

        if file_last_updated > (cached['timestamp'] + MAX_CACHE_AGE):
            logging.debug('Cache too old: regenerating cache')
            regen = True

    except IOError:
        logging.error('Error opening %s: regenerating cache' % cache_filename)
        regen = True
    """

    # Cache too old, run query
    if regen:
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

        """
        # Update cache file
        data = {'results': resultset, 'timestamp': file_last_updated}
        with open(cache_filename, 'w') as cache:
            pickle.dump(data, cache)
        """

    # Cached data is fresh enough, use that
    resultset = cached['results']
    return resultset

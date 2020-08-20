import os
import time
import pickle
from json import load
from mysql import connector

conn = connector.connect(
    host=os.environ.get('MYSQL_HOST'),
    user=os.environ.get('MYSQL_USERNAME'),
    password=os.environ.get('MYSQL_PASSWORD')
)

## READ THIS: https://stackoverflow.com/questions/307438/how-can-i-tell-when-a-mysql-table-was-last-updated
## AND THIS:  https://stackoverflow.com/questions/15749719/caching-mysql-query-returned-by-python-script

MAX_CACHE_AGE = 60*20               # 20 Minutes
file_last_updated = time.time()

def execute_query(query, cache_filename):
    '''
    Executes the SELECT query on MYSQL database

    Arguments:
        query {str} -- Query to execute
        cache_filname {str} -- Cache filename for the respective Query
    Returns:
        {list} -- Resultset as a pandas DataFrame
    '''
    regen = False
    try:
        with open(cache_filename, 'r') as cache:
            cached = pickle.load(cache)

        if file_last_updated > (cached['timestamp'] + MAX_CACHE_AGE):
            print("Cache too old: regenerating cache")
            regen = True
        else:
            print("Cached data is fresh enough: loading results from cache")

    except IOError:
        print("Error opening %s: regenerating cache" % cache_filename)
        regen = True

    if regen:
        # Cache too old, run query
        cursor = conn.cursor()
        cursor.execute(query)
        resultset = cursor.fetchall()
        cursor.close()

        # Update cache file
        data = {'results': resultset, 'timestamp': file_last_updated}
        with open(cache_filename, 'w') as cache:
            pickle.dump(data, cache)
    else:
        # Cached data is fresh enough, use that
        resultset = cached['results']
    return resultset


def get_state_frt(state:str):
    """
    Get FRT details for a single state.

    Arguments:
        state {str} -- Name of the state.
    Returns:
        {JSON} -- Returns headers of the columns and data in list
    """

    if not state:
        return None

    elif state == 'India':
        query = """
            SELECT
                '{state}' AS state
                , frt.face_recognition_system AS name
                , frt.status AS status
                , frt.purpose AS purpose
                , frt.reported_use AS reported_use
                , frt.rti_date AS rti_date
                , frt.financial_outlay AS financial_outlay
                , frt.authority AS authority
            FROM
                panoptic.frt AS frt
        """.format(
            state=state
        )

    else:
        query = """
            SELECT
                '{state}' AS state
                , frt.face_recognition_system AS name
                , frt.status AS status
                , frt.purpose AS purpose
                , frt.reported_use AS reported_use
                , frt.rti_date AS rti_date
                , frt.financial_outlay AS financial_outlay
                , frt.authority AS authority
            FROM
                panoptic.place AS place
            LEFT JOIN
                panoptic.frt_place_link AS link
            ON
                place.id = link.place__key
            LEFT JOIN
                panoptic.frt AS frt
            ON
                link.frt__key = frt.id
            WHERE
                place.state = '{state}'
        """.format(
            state=state
        )

    return execute_query(query)


def get_total_frt(state:str):
    """
    Get total number of FRTs for a single state.

    Arguments:
        state {str} -- Name of the state.
    Returns:
        {JSON} -- Returns headers of the columns and data in list
    """
    if not state:
        return None

    elif state == 'India':
        query = """
            SELECT
                'India' AS state
                , COUNT(DISTINCT frt.id) AS count
            FROM
                panoptic.frt AS frt
        """

    else:
        query = """
            SELECT
                '{state}' AS state
                , COUNT(DISTINCT frt.id) AS count
            FROM
                panoptic.place AS place
            LEFT JOIN
                panoptic.frt_place_link AS link
            ON
                place.id = link.place__key
            LEFT JOIN
                panoptic.frt AS frt
            ON
                link.frt__key = frt.id
            WHERE
                place.state = '{state}'
        """.format(
            state=state
        )

    return execute_query(query)

def get_single_state_frt(state:str = None):
    """
    Get FRT details for a single state.

    Arguments:
        state {str} -- Name of the state. Defaults to India
    Returns:
        {list} -- List of dictionary of the results
        {
            "state": "",
            "name": "",
            "status": "",
            "purpose": "",
            "reported_use": "",
            "rti_date": "",
            "financial_outlay": "",
            "authority": ""
        }
    """

    # Check if state was provided as a parameter.
    if 'state' == None:
        state = 'India'

    return utils.get_state_frt(state=state)


def get_state_total_frt(state:str = None):
    """
    Get total number of FRTs in a state.

    Arguments:
        state {str} -- Name of the state. Defaults to India
    Returns:
        {dict} -- Dictionary of the result
        {
            "state": "",
            "count": ""
        }
    """

    # Check if state was provided as part of the URL.
    if 'state' == None:
        state = 'India'

    return utils.get_total_frt(state=state)

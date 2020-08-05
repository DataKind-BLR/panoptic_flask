import os
from json import load
from mysql import connector

conn = connector.connect (
    host = os.environ.get('MYSQL_HOST'),
    user = os.environ.get('MYSQL_USERNAME'),
    password = os.environ.get('MYSQL_PASSWORD')
)
cursor = conn.cursor()

def execute_select_query(query:str):
    """
    Executes the SELECT query on MYSQL database

    Arguments:
        query {str} -- Query to execute
    Returns:
        {list} -- Columns returned by the query
        {list} -- List of data returned by the query
    """
    cursor.execute(query)

    # Get all the columns of data
    headers = [x[0] for x in cursor.description]
    data = cursor.fetchall()

    conn.close()

    return headers, data

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

    results = []

    headers, data = execute_select_query(query)

    while data:
        results.append(dict(zip(headers, data.pop())))

    return results


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

    headers, data = execute_select_query(query)

    while data:
        result = dict(zip(headers, data.pop()))

    return result


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

"""Utilities function for processing data"""
from model.db_helper import execute_select_query


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
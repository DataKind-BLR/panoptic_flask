from db_connector import execute_select_query

def get_frt(state:str):
    """
    Accepts state

    Returns headers of the columns and data in list
    """
    if not state:
        return None, None

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
        """

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

    return execute_select_query(query)


def get_total_frt(state:str):
    """
    Accepts state name

    Returns total number of FRTs in the state mentioned
    """
    if not state:
        return None, None

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

    return execute_select_query(query)
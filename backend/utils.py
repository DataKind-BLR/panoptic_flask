from backend.db_helper import execute_select_query

def _sum_state_financial_outlay(results:dict):
    """
    Aggregate state total financial outlay for FRT

    Arguments:
        results {dict} -- Result set from `get_state_frts`
    Returns:
        float -- Returns total financial outlay
    """
    if results == None:
        return 0

    total_financial_outlay = 0

    for result in results:
        if result['financial_outlay_cr']:
            total_financial_outlay += result['financial_outlay_cr']

    return total_financial_outlay


def _count_frt_use(results:dict):
    """
    Get state total financial outlay for FRT

    Arguments:
        results {dict} -- Result set from `get_state_frts`
    Returns:
        int -- Returns the number of FRTs that are in use
        int -- Returns the number of FRTs that are not in use
    """
    if results == None:
        return 0

    total_in_use = 0
    total_not_in_use = 0

    for result in results:
        if result['in_use'] == True:
            total_in_use += 1
            continue

        total_not_in_use += 1

    return total_in_use, total_not_in_use


def get_state_frts(state:str):
    """
    Get FRT details for a single state.

    Arguments:
        state {str} -- Name of the state.
    Returns:
        {JSON} -- Returns headers of the columns and data in list
    """

    query = """
        SELECT
            frt.face_recognition_system AS name
            , (
                CASE
                    WHEN frt.status = 'In use' THEN True
                    ELSE False
                END
            ) AS in_use
            , frt.purpose AS purpose
            , frt.reported_use AS report_use_on
            , frt.rti_date AS rti_filed_on
            , ROUND((frt.financial_outlay/10000000.0), 2) AS financial_outlay_cr
            , media_source.link AS media_source
            , rti_source.link AS rti_response
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
        LEFT JOIN
            panoptic.external_links AS media_source
        ON
            frt.id = media_source.frt__key
            AND media_source.link_type = 'Media source'
        LEFT JOIN
            panoptic.external_links AS rti_source
        ON
            frt.id = rti_source.frt__key
            AND rti_source.link_type = 'RTI Replies'
        WHERE
            place.state = '{state}'
    """.format(
        state=state
    )


    headers, data = execute_select_query(query)

    results = []
    while data:
        results.append(dict(zip(headers, data.pop())))

    return results


def get_count_frt_jurisdiction():
    """
    Get FRT types deployed

    Arguments:
    Returns:
        int -- Returns the number of FRTs that are national
        int -- Returns the number of FRTs that are state level
    """

    query = """
        SELECT
            COUNT(
                DISTINCT(
                    CASE
                        WHEN
                            frt.jurisdiction = 'State' THEN frt.id
                        ELSE NULL
                    END
                )
            ) AS state_frt
            , COUNT(
                DISTINCT(
                    CASE
                        WHEN
                            frt.jurisdiction = 'Central' THEN frt.id
                        ELSE NULL
                    END
                )
            ) AS central_frt
        FROM
            panoptic.frt AS frt
    """

    headers, data = execute_select_query(query)

    if headers and data:
        results = dict(zip(headers, data.pop()))
        return results['state_frt'], results['central_frt']

    return 0, 0



def _sum_frts(results:dict):
    """
    Get total number of FRTs

    Arguments:
        results {dict} -- Result set from `get_total_frts`
    Returns:
        int -- Total number of FRTs in the nation
    """
    if results == None:
        return 0

    total_frts = 0

    for result in results:
        if result['state_total']:
            total_frts += result['state_total']

    return total_frts


def get_total_frts():
    """
    Get total number of FRTs for a single state.

    Arguments:
    Returns:
        {JSON} -- Returns headers of the columns and data in list
    """

    query = """
        SELECT
            place.state AS state
            , COUNT(DISTINCT frt.id) AS state_total
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
        GROUP BY
            place.state
    """

    headers, data = execute_select_query(query)

    results = []
    while data:
        results.append(dict(zip(headers, data.pop())))

    return results

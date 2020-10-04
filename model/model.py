from model import utils


def get_home_page_data():
    """
    Get home page data to display in the map.
    Returns:
        {dict} - Dictionary of the result
        {
            'total_frts': int,
            'total_frts_national': int,
            'total_frts_states': int,
            'states': [{
                'state': str,
                'state_total': int
            }]
        }
    """

    total_frts = utils.get_total_frts()
    total_frts_states, total_frts_national = utils.get_count_frt_jurisdiction()
    result = {
        'total_frts': utils._sum_frts(total_frts),
        'total_frts_national': total_frts_states,
        'total_frts_states': total_frts_national,
        'states': total_frts
    }

    return result


def get_state_page_data(state: str):
    """
    Arguments:
        state {str} -- Name of the state.
    Returns:
        {dict} - Dictionary of the result
        {
            'name': str,
            'total_frts': int,
            'total_in_use': int,
            'total_not_in_use': int,
            'financial_outlay_cr': float,
            'frts': [{
                'name': str,
                'in_use': bool,
                'purpose': str,
                'report_use_on': str,
                'rti_filed_on': timestamp,
                'financial_outlay_cr': float,
                'media_source': str,
                'rti_response': str
            }]
        }
    """

    if 'state' is None:
        return None

    state_frts = utils.get_state_frts(state=state)
    frts_in_use, frts_not_in_use = utils._count_frt_use(state_frts)
    statewise_total_frts = utils.get_total_frts()

    total_frts = 0
    for stf in statewise_total_frts:
        if stf['state'] == state:
            total_frts = stf['state_total']

    result = {
        'name': state,
        'total_frts': total_frts,
        'total_in_use': frts_in_use,
        'total_not_in_use': frts_not_in_use,
        'financial_outlay_cr': utils._sum_state_financial_outlay(state_frts),
        'frts': state_frts
    }

    return result

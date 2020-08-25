"""Model file for accessing the base functions"""
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

    result = {
        'total_frts': utils._sum_frts(total_frts),
        'total_frts_national': 0,
        'total_frts_states': 0,
        'states': total_frts
    }

    return result


def get_state_page_data(state:str):
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

    if 'state' == None:
        return None

    state_frts = utils.get_state_frts(state=state)
    frts_in_use, frts_not_in_use = utils._count_frt_use(state_frts)

    result = {
        'name': state,
        'total_frts': len(state_frts),
        'total_in_use': frts_in_use,
        'total_not_in_use': frts_not_in_use,
        'financial_outlay_cr': utils._sum_state_financial_outlay(state_frts),
        "frts": state_frts
    }

    return result

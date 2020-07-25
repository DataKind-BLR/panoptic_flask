"""Model file for accessing the base functions"""
from model import utils

def single_frt(state:str = None):
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

    return utils.get_frt(state=state)

def total_frt(state:str = None):
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

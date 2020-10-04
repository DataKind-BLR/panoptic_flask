import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import credential_json_path, scope, source
from random import randint

def random_with_N_digits(n):
    '''
    Random number generator
    '''
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def get_spreadsheet():
    '''
    Method to get the spreadsheet object from the Gsheets API.
    '''
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        credential_json_path, scopes=scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open(source)
    return spreadsheet



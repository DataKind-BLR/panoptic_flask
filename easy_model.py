import pandas as pd
from mysql import connector

conn = connector.connect(
    host='localhost',
    user='root',
    password='admin123',
    database='panoptic'
)
df_frts = pd.read_sql('SELECT * FROM frts_by_places', conn)


def get_home_page_data():
    total_in_use = df_frts[df_frts['in_use'] == 1]['in_use'].count()
    total_not_in_use = df_frts[df_frts['in_use'] == 0]['in_use'].count()

    return {
        'total_frts': df_frt.count()[0],
        'total_frts_central': total_frts_central,
        'total_frts_states': df_frts['state'].value_counts().sum(),
        'total_financial_outlay': df_frts['financial_outlay_cr'].sum(),
        'states': df_frts['state'].value_counts().to_dict()
    }


def get_state_details(state):
    state_df = df_frts[df_frts['state'] == state]
    if state_df.empty():
        print('No data exists for ', state)
        return False
    return {
        frts: state_df.to_dict(orient='records')
    }

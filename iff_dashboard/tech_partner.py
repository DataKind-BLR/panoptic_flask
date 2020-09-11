from gsheets_utils import random_with_N_digits
from config import conn


class TechPartner():

    def __init__(self, _id, technology_partner, website, roc_details, upload_status):
        self.id = _id if _id else random_with_N_digits(8)
        self.technology_partner = technology_partner
        self.website = website
        self.upload_status = upload_status
        self.roc_details = roc_details

    def insert_to_tech_partners(self):

        query = ''' INSERT INTO
                        panoptic.technology_partner (
                            id, technology_partner, website, roc_details)
                    VALUES
                        ({id}, '{technology_partner}', '{website}', '{roc_details}')
                    ON DUPLICATE KEY UPDATE
                        technology_partner = '{technology_partner}',
                        website = '{website}',
                        roc_details = '{roc_details}'
                    ''' .format_map({'id': self.id,
                                     'technology_partner': self.technology_partner,
                                     'website': self.website,
                                     'roc_details': self.roc_details})
    
        insert_cursor = conn.cursor()
        insert_cursor.execute(query)
        conn.commit()
        insert_cursor.close()

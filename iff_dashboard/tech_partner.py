from gsheets_utils import random_with_N_digits
from db_utils import conn


class TechPartner():

    def __init__(self, _id, technology_partner, website, upload_status):
        self.id = _id if _id else random_with_N_digits(8)
        self.technology_partner = technology_partner
        self.website = website
        self.upload_status = upload_status

    def insert_to_tech_partners(self, id_, technology_partner, website):

        query = ''' INSERT INTO
                        panoptic.technology_partner (
                            id, technology_partner, website)
                    VALUES
                        ({id}, '{technology_partner}', '{website}')
                    ON DUPLICATE KEY UPDATE
                        technology_partner = '{technology_partner}',
                        website = '{website}'
                    ''' .format_map({'id': self.id,
                                     'technology_partner': self.technology_partner,
                                     'website': self.website})

        insert_cursor = conn.cursor()
        insert_cursor.execute(query)
        conn.commit()
        insert_cursor.close()

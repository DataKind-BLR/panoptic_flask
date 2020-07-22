from gsheets_utils import random_with_N_digits
from db_utils import conn


class Frt:

    def __init__(self,
                 _id,
                 authority,
                 face_recognition_system,
                 jurisdiction,
                 states,
                 upload_status,
                 purpose,
                 technology_partner,
                 tender_publication_date,
                 reported_use_date,
                 status,
                 linked_databases,
                 financial_outlay,
                 prescribed_technical_standards,
                 storage_duration,
                 legal_basis,
                 link_govt_sourced,
                 link_media_sourced,
                 rti_status,
                 rti_replies,
                 rti_date):

        self.id = _id if _id else random_with_N_digits(8)
        self.authority = authority
        self.face_recognition_system = face_recognition_system
        self.jurisdiction = jurisdiction
        self.states = states
        self.upload_status = upload_status
        self.purpose = purpose
        self.technology_partner = technology_partner
        self.tender_publication_date = tender_publication_date
        self.reported_use_date = reported_use_date
        self.status = status
        self.linked_databases = linked_databases.rstrip()
        self.financial_outlay = financial_outlay
        self.prescribed_technical_standards = prescribed_technical_standards
        self.storage_duration = storage_duration
        self.legal_basis = legal_basis
        self.link_govt_sourced = link_govt_sourced
        self.link_media_sourced = link_media_sourced
        self.rti_status = rti_status
        self.rti_replies = rti_replies
        self.rti_date = rti_date
        self.technology_partner__key = self.get_technology_partner_key(
            self.technology_partner)

    def get_technology_partner_key(self, technology_partner):
        cursor = conn.cursor()
        cursor.execute(
            "select id from panoptic.technology_partner where technology_partner = '{}';".format(technology_partner))
        tech_partner, = cursor.fetchone()
        cursor.close()

        return tech_partner

    def get_place_id(self, state):

        cursor = conn.cursor()
        cursor.execute(
            "select id from panoptic.place where state='{}'".format(state))
        state, = cursor.fetchone()
        cursor.close()
        return state

    def update_frt_place_table(self):
        insert_cursor = conn.cursor()

        for state in self.states.split(','):
            place_key = self.get_place_id(state)
            query = ''' INSERT INTO panoptic.frt_place_link (frt__key, place__key) \
                            VALUES ({frt_key},{place_key})'''.format_map({
                'frt_key': self.id, 'place_key': place_key})
            insert_cursor.execute(query)
            conn.commit()
        insert_cursor.close()

    def insert_to_frt_table(self):
        query = '''INSERT INTO \
                        panoptic.frt (id, \
                                    authority,\
                                    face_recognition_system,\
                                    purpose,\
                                    technology_partner__key,\
                                    status,\
                                    linked_databases, \
                                    financial_outlay,\
                                    prescribed_technical_standards,\
                                    storage_duration, \
                                    legal_basis, tender_publication_date,rti_date,reported_use)\
                        VALUES\
                        ({},'{}','{}','{}',{},'{}','{}','{}','{}','{}', '{}','{}', '{}','{}') '''.format(self.id,
                                                                                                         self.authority,
                                                                                                         self.face_recognition_system,
                                                                                                         self.purpose,
                                                                                                         self.technology_partner__key,
                                                                                                         self.status,
                                                                                                         self.linked_databases,
                                                                                                         self.financial_outlay,
                                                                                                         self.prescribed_technical_standards,
                                                                                                         self.storage_duration,
                                                                                                         self.legal_basis,
                                                                                                         self.tender_publication_date,
                                                                                                         self.rti_date,
                                                                                                         self.reported_use_date
                                                                                                         )

        insert_cursor = conn.cursor()
        insert_cursor.execute(query)
        conn.commit()
        insert_cursor.close()

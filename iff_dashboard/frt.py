from gsheets_utils import random_with_N_digits
from config import conn
import re


class Frt:
    '''
    The class FRT has all the attributes of a FRT and the methods to update,add and
    delete the changes from the spreadsheet.
    
    '''
    def __init__(self,
                 _id,
                 authority,
                 face_recognition_system,
                 jurisdiction,
                 place,
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
                 rti_status = None,
                 rti_file_date = None,
                 rti_replies = None,
                 rti_reply_date  = None):

        self.id = _id if _id else random_with_N_digits(8)
        self.authority = authority
        self.place = place
        self.face_recognition_system = face_recognition_system
        self.jurisdiction = jurisdiction
        self.states = [state for state in states.split(', ') if state]
        self.upload_status = upload_status
        self.purpose = purpose
        self.technology_partner = technology_partner
        self.tender_publication_date = tender_publication_date
        self.reported_use_date = reported_use_date
        self.status = status
        self.linked_databases = linked_databases.rstrip()
        self.financial_outlay = financial_outlay.replace(',', '') if financial_outlay else 'NULL'
        self.prescribed_technical_standards = prescribed_technical_standards
        self.storage_duration = storage_duration
        self.legal_basis = legal_basis
        self.link_govt_sourced = link_govt_sourced
        self.link_media_sourced = link_media_sourced
        self.rti_status = rti_status
        self.rti_file_date = rti_file_date
        self.rti_replies = rti_replies
        self.rti_reply_date = rti_reply_date
        self.technology_partner__key = self.get_technology_partner_key(self.technology_partner)

    def get_technology_partner_key(self, technology_partner):
        cursor = conn.cursor()
        cursor.execute(
            "select id from panoptic.technology_partner where technology_partner = '{}';".format(technology_partner))
        tech_partner = cursor.fetchone()
        cursor.close()

        return tech_partner[0] if tech_partner else 'NULL'

    def get_place_id(self, state):

        cursor = conn.cursor()
        cursor.execute(
            "select id from panoptic.place where state='{}'".format(state))
        res = cursor.fetchone()
        state = res[0] if res else None
        cursor.close()
        return state

    def get_state_ids(self):
        cursor = conn.cursor()
        cursor.execute(
            "select place__key from panoptic.frt_place_link where frt__key  = {} ".format(self.id))
        result = cursor.fetchall()
        cursor.close()
        state_ids = set([row[0] for row in result])
        return state_ids

    def add_place_id(self, place_key):
        insert_cursor = conn.cursor()
        query = ''' INSERT INTO panoptic.frt_place_link (frt__key, place__key) \
                            VALUES ({frt_key},{place_key})'''.format_map({
            'frt_key': self.id, 'place_key': place_key})
        insert_cursor.execute(query)
        conn.commit()
        insert_cursor.close()

    def delete_place_id(self, place_key):
        insert_cursor = conn.cursor()
        query = ''' DELETE FROM  panoptic.frt_place_link \
                            WHERE frt__key = {frt_key} and place__key = {place_key} '''.format_map({
            'frt_key': self.id, 'place_key': place_key})
        insert_cursor.execute(query)
        conn.commit()
        insert_cursor.close()

    def update_frt_place_table(self):
        db_state_ids = self.get_state_ids()
        gsheets_states = set([self.get_place_id(state)
                              for state in self.states])
        for place_id in gsheets_states - db_state_ids:
            self.add_place_id(place_id)

        for place_id in db_state_ids - gsheets_states:
            self.delete_place_id(place_id)

    def add_rti_replies(self):
        if self.rti_replies:
            query = '''
                    INSERT INTO panoptic.external_links(link, link_type, frt__key)
                    SELECT * FROM (SELECT '{link}', '{link_type}', {frt__key}) AS tmp
                    where NOT EXISTS (SELECT link, link_type, frt__key from panoptic.external_links 
                                        WHERE frt__key = '{frt__key}'  
                                        AND link_type = '{link_type}'
                                        AND link = '{link}')
            '''.format_map({'link': self.rti_replies,
                            'link_type': 'RTI Replies',
                            'frt__key': self.id})
            print(query)
            insert_cursor = conn.cursor()
            insert_cursor.execute(query)
            conn.commit()
            insert_cursor.close()

    def add_govt_link(self):
        if self.link_govt_sourced:
            query = '''
                    INSERT INTO panoptic.external_links(link, link_type, frt__key)
                    SELECT * FROM (SELECT '{link}', '{link_type}', {frt__key}) AS tmp
                    where NOT EXISTS (SELECT link, link_type, frt__key from panoptic.external_links 
                                        WHERE frt__key = '{frt__key}'  
                                        AND link_type = '{link_type}'
                                        AND link = '{link}')
            '''.format_map({'link': self.link_govt_sourced,
                            'link_type': 'Govt Source',
                            'frt__key': self.id})
            insert_cursor = conn.cursor()
            insert_cursor.execute(query)
            conn.commit()
            insert_cursor.close()
    
    def add_media_link(self):
        if self.link_media_sourced:
            query = '''
                    INSERT INTO panoptic.external_links(link, link_type, frt__key)
                    SELECT * FROM (SELECT '{link}', '{link_type}', {frt__key}) AS tmp
                    where NOT EXISTS (SELECT link, link_type, frt__key from panoptic.external_links 
                                        WHERE frt__key = '{frt__key}'  
                                        AND link_type = '{link_type}'
                                        AND link = '{link}')
            '''.format_map({'link': self.rti_replies,
                            'link_type': 'Media Source',
                            'frt__key': self.id})
            insert_cursor = conn.cursor()
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
                                    legal_basis, tender_publication_date,rti_date,reported_use, jurisdiction,\
                                    rti_status, rti_reply_date)\
                        VALUES\
                        	({id},'{authority}','{face_recognition_system}','{purpose}',{technology_partner__key}, \
                        	'{status}','{linked_databases}',{financial_outlay},'{prescribed_technical_standards}', \
                        	'{storage_duration}', '{legal_basis}','{tender_publication_date}', {rti_date},'{reported_use}', 
                            '{jurisdiction}', '{rti_status}', {rti_reply_date})
                         ON DUPLICATE KEY UPDATE
                            id = {id},
                            authority = '{authority}',
                            face_recognition_system = '{face_recognition_system}',
                            purpose = '{purpose}',
                            technology_partner__key = {technology_partner__key},
                            status = '{status}',
                            linked_databases = '{linked_databases}',
                            financial_outlay = {financial_outlay},
                            prescribed_technical_standards = '{prescribed_technical_standards}',
                            storage_duration = '{storage_duration}',
                            legal_basis = '{legal_basis}',
                            tender_publication_date = '{tender_publication_date}',
                            rti_date = {rti_date},
                            reported_use = '{reported_use}',
                            jurisdiction = '{jurisdiction}',
                            rti_status = '{rti_status}',
                            rti_reply_date = {rti_reply_date}
                         '''.format_map({'id': self.id,
                                         'authority': self.authority,
                                         'face_recognition_system': self.face_recognition_system,
                                         'purpose': self.purpose,
                                         'technology_partner__key': self.technology_partner__key,
                                         'status': self.status,
                                         'linked_databases': self.linked_databases,
                                         'financial_outlay': self.financial_outlay,
                                         'prescribed_technical_standards': self.prescribed_technical_standards,
                                         'storage_duration': self.storage_duration,
                                         'legal_basis': self.legal_basis,
                                         'tender_publication_date': self.tender_publication_date,
                                         'rti_date': "'{}'".format(self.rti_file_date) if self.rti_file_date else 'NULL',
                                         'reported_use': self.reported_use_date,
                                         'jurisdiction': self.jurisdiction,
                                         'rti_status': self.rti_status,
                                         'rti_reply_date': "'{}'".format(self.rti_reply_date) if self.rti_reply_date else 'NULL'

                                         })
        insert_cursor = conn.cursor()
        insert_cursor.execute(query)
        conn.commit()
        insert_cursor.close()

    
    def delete_frt(self):
        query = ''' 
            DELETE FROM  panoptic.frt_place_link WHERE frt__key = {frt_key}
            '''.format_map({'frt_key': self.id})

        query1 = ''' 
            DELETE FROM  panoptic.external_links WHERE frt__key = {frt_key}
            '''.format_map({'frt_key': self.id})

        query2 = ''' 
            DELETE FROM  panoptic.frt WHERE id = {frt_key}
            '''.format_map({'frt_key': self.id})

        delete_cursor = conn.cursor()
        delete_cursor.execute(query)
        delete_cursor.execute(query1)
        delete_cursor.execute(query2)
        conn.commit()
        delete_cursor.close()
        
        
        


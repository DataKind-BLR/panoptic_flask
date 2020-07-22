
import mysql.connector
from config import DB_USER, DB_PASSWORD


def connection():
    conn = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD
    )

    return conn


conn = connection()


def insert_to_tech_partners(id_, technology_partner, website):

    query = ''' INSERT INTO
                    panoptic.technology_partner (
                        id, technology_partner, website)
                VALUES
                    ({id}, '{technology_partner}', '{website}')
                ON DUPLICATE KEY UPDATE
                    technology_partner = '{technology_partner}',
                    website = '{website}'
                 ''' .format_map({'id': id_,
                                  'technology_partner': technology_partner,
                                  'website': website})

    insert_cursor = conn.cursor()
    insert_cursor.execute(query)
    conn.commit()
    insert_cursor.close()


def insert_to_location(id_, state):

    query = ''' INSERT INTO
                    panoptic.place (id,
                         state, country)
                VALUES
                    ({id}, '{state}', 'India')
                 ''' .format_map({'id': id_, 'state': state})

    insert_cursor = conn.cursor()
    insert_cursor.execute(query)
    conn.commit()
    insert_cursor.close()

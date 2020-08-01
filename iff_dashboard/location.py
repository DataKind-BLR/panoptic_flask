from config import conn


class Location():
    def __init__(self, _id, state):
        self.id = _id
        self.state = state
        self.country = 'India'

    def insert_to_location(self):

        query = ''' INSERT INTO
                        panoptic.place (id,
                            state, country)
                    VALUES
                        ({id}, '{state}', '{country}')
		    ON DUPLICATE KEY UPDATE
                        id = '{id}',
                        state = '{state}',
                        country = '{country}'

                    ''' .format_map({'id': self.id, 'state': self.state, 'country': self.country})

        insert_cursor = conn.cursor()
        insert_cursor.execute(query)
        conn.commit()
        insert_cursor.close()

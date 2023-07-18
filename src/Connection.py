import psycopg2


class DAO:
    def __init__(self):
        self.conn = psycopg2.connect("dbname=app user=postgres password=1221909128 host=localhost")

        if self.conn.status:
            print('Successfully connected')
        else:
            print('Connection corrupted')

        self.cur = self.conn.cursor()

    def exec(self, query):
        self.cur.execute(query)

    def getFromSelect(self):
        return self.cur.fetchall()

    def getColumnNames(self, tableName):
        self.cur.execute('Select * FROM ' + tableName + ' LIMIT 0')
        colnames = [desc[0] for desc in self.cur.description]
        return colnames

    def __del__(self):
        self.cur.close()
        self.conn.close()

import psycopg2
from src.config import connectionString

class DAO:
    def __init__(self):
        self.conn = psycopg2.connect(connectionString)

        if self.conn.status:
            print('Успешное подключение к БД')
        else:
            print('Подключение к БД не удалось установить')

        self.cur = self.conn.cursor()

    def exec(self, query):
        self.cur.execute(query)
        self.save()

    def save(self):
        self.conn.commit()

    def getFromSelect(self):
        return self.cur.fetchall()

    def getColumnNames(self, tableName):
        self.cur.execute('Select * FROM ' + tableName + ' LIMIT 0')
        colnames = [desc[0] for desc in self.cur.description]
        return colnames

    def __del__(self):
        self.cur.close()
        self.conn.close()

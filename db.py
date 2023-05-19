import mysql.connector as mysql

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        self.db = mysql.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )
        self.cursor = self.db.cursor()
    
    def execute(self, query, values):
        self.connect()
        self.cursor.execute(query, values)

        self.db.commit()
        return True

    def fetch(self, query):
        self.connect()
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data
    
    def disconnect(self):
        self.db.close()

    def get_all(self):
        query = "SELECT * FROM `data`"
        return self.fetch(query)

    def get_by_id(self, id):
        query = "SELECT * FROM `data` WHERE `id` = %s"
        values = (id, )
        return self.fetch(query, values)
import pymysql

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            db = 'GOOGLE_SCHOLAR'
        )
        
        self.cursor = self.connection.cursor()
        print("Conexion establecida satisfactoriamente!!")

#database = Database()

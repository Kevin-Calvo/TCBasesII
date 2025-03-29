import psycopg2
import os

class databaseController():
    def __init__(self):
        pass

    def conectar_base_datos(self):
        try :
            connection=psycopg2.connect(
                host = os.getenv("DB_HOST"),
                port = os.getenv("BD_PORT"),
                user = os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            return connection
        except Exception as ex:
            return ex
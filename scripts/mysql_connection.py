import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Farheen2005",
        database = "kps_knowledge_base"
    )

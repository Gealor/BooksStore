import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from core.models.base import Base
from core.models.db_helper import db_helper
from core.config import settings

def create_database():
    conn = psycopg2.connect(
        # в dbname введите существующую базу данных в вашей СУБД, к которой можно подключиться
        dbname = "postgres", 
        user = settings.db.user, 
        password = settings.db.password,
        host = settings.db.host,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE {settings.db.name}")
    print("База данных создана")
    cur.close()
    conn.close()
    
if __name__=="__main__":
    create_database()
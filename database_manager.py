import psycopg2
from dotenv import load_dotenv
import os 

load_dotenv()
DB_CONFIG = {
    'host' : os.getenv("DB_HOST"),
    'dbname' : os.getenv("DB_NAME"),
    'user' : os.getenv("DB_USER"),
    'password' : os.getenv("DB_PASS"),
    'port' : os.getenv("DB_PORT")
}


def get_db_connection(DB_CONFIG):
    conn=None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        # print("Connect to PostgreSQL database successfully")
        return conn
    except psycopg2.Error as e:
        print(f"[ERROR] Failed to connect to Database : {e}")
        exit(1)

get_db_connection(DB_CONFIG)
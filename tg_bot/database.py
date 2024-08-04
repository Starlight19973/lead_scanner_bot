import psycopg2
from config import DATABASE


def execute_query(query, params=()):
    try:
        conn = psycopg2.connect(**DATABASE)
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")


def fetch_query(query, params=()):
    try:
        conn = psycopg2.connect(**DATABASE)
        cur = conn.cursor()
        cur.execute(query, params)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

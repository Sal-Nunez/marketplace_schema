import pymysql.cursors
from flask_app import DB

def query_db(query, data=None):
    connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = 'root', 
            db = DB,
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor,
            autocommit = True
        )
    with connection.cursor() as cursor:
        try:
            query = cursor.mogrify(query, data)
            print("Running Query:", query)
            cursor.execute(query)
            if query.lower().startswith("select"):
                return cursor.fetchall()
            if query.lower().startswith("insert"):
                return cursor.lastrowid
        except Exception as e:
            print("Something went wrong", e)
            return False
        finally:
            connection.close()
import datetime
import json
import psycopg2
import psycopg2.extras
from ..record import Record
from ..utils.hiddenid import hash_to_int
def create_conn():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="genjson",
            user="postgres",
            password="psql"
        )
        return conn
    except psycopg2.Error as e:
        print(e)

conn = create_conn()

def extract_id(key):
    if isinstance(key, str):
        return hash_to_int(key)
    else:
        return key

class DbSync:
    def __init__(self, modelClass, table):
        self.conn = conn
        self.table = "data"
        self.model_class = modelClass
        self.model_name = modelClass.__name__

    def __all__(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(f"SELECT * FROM {self.table} where model = '{self.model_name}'")
            rows = cur.fetchall()
            return [Record(**row) for row in rows]

    def __getitem__(self, key):
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if isinstance(key, list) or isinstance(key, tuple):
                ids = [extract_id(k) for k in key]
                placeholder = ','.join(['%s'] * len(ids))
                cur.execute(f"SELECT * FROM {self.table} WHERE id IN ({placeholder})", ids)
                rows = cur.fetchall()
                return [Record(**row) for row in rows]
            if isinstance(key, slice):
                query = f"SELECT * FROM {self.table}"
                (start, stop) = extract_id(key.start), extract_id(key.stop)
                insertions = []
                if start or stop:
                    query +=  f" WHERE "
                if start:
                    query += f"id >= %s"
                    insertions.append(start)
                    if stop:
                        query += " and "
                if stop:
                    query += f"id < %s"
                    insertions.append(stop)
                cur.execute(query, insertions)
                rows = cur.fetchall()
                return [Record(**row) for row in rows]
            else:
                id = extract_id(key)
                cur.execute(f"SELECT * FROM {self.table} WHERE id = %s", (id,))
                row = cur.fetchone()
                if row is None:
                    raise KeyError
                record = Record(**row)
                return record

    def __setitem__(self, key, value):
        if key in self:
            return self.update(key, value)
    
    def __lshift__(self, value):
        self.insert(value)

    def __delitem__(self, key):
        id = extract_id(key)
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(f"DELETE FROM {self.table} WHERE id = %s", (id,))
            if cur.rowcount == 0:
                raise KeyError
        self.conn.commit()
        

    def __contains__(self, key):
        id = extract_id(key)
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(f"SELECT 1 FROM {self.table} WHERE id = %s", (id,))
            return bool(cur.fetchone())

    def insert(self, model_instance):
        sql = f"INSERT INTO {self.table} (model, content) VALUES (%s, %s) RETURNING *"
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql,  (model_instance.__class__.__name__, model_instance.json()))
            row = cur.fetchone()
            rec = Record(**row)
        self.conn.commit()
        return rec

    def update(self, key, model_instance):
        model = model_instance.__class__.__name__
        content = model_instance.json()
        id = extract_id(key)
        sql = f"UPDATE {self.table} SET model = %s, content = %s, updated_at = %s WHERE id = %s"
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, (model, content, datetime.datetime.now(), id))
        self.conn.commit()
        
def get_db_sync(model):
    return DbSync(model, "data")
from contextlib import contextmanager

from aiosql_mysql import utilities


class PyMySQLAdaptor:
    @staticmethod
    def process_sql(_query_name, _op_type, sql):
        return utilities.sql_to_print_style(sql)

    @staticmethod
    def select(conn, _query_name, sql, parameters, record_class=None):
        with conn.cursor() as cur:
            cur.execute(sql, parameters)
            results = cur.fetchall()
            if record_class is not None:
                column_names = [c.name for c in cur.description]
                results = [
                    record_class(**dict(zip(column_names, row))) for row in results
                ]
        return results

    @staticmethod
    def select_one(conn, _query_name, sql, parameters, record_class=None):
        with conn.cursor() as cur:
            cur.execute(sql, parameters)
            result = cur.fetchone()
            if result is not None and record_class is not None:
                column_names = [c.name for c in cur.description]
                result = record_class(**dict(zip(column_names, result)))
        return result

    @staticmethod
    def select_value(conn, _query_name, sql, parameters):
        with conn.cursor() as cur:
            cur.execute(sql, parameters)
            result = cur.fetchone()
        return result[0] if result else None

    @staticmethod
    @contextmanager
    def select_cursor(conn, _query_name, sql, parameters):
        with conn.cursor() as cur:
            cur.execute(sql, parameters)
            yield cur

    @staticmethod
    def insert_update_delete(conn, _query_name, sql, parameters):
        with conn.cursor() as cur:
            cur.execute(sql, parameters)

    @staticmethod
    def insert_update_delete_many(conn, _query_name, sql, parameters):
        with conn.cursor() as cur:
            cur.executemany(sql, parameters)

    @staticmethod
    def insert_returning(conn, _query_name, sql, parameters):
        with conn.cursor() as cur:
            cur.execute(sql, parameters)
            res = cur.fetchone()
            if res:
                return res[0] if len(res) == 1 else res
            else:
                return None

    @staticmethod
    def execute_script(conn, sql):
        with conn.cursor() as cur:
            cur.execute(sql)

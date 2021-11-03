from aiosql_mysql import utilities
from contextlib2 import asynccontextmanager

from asyncmy.cursors import DictCursor


class AsyncMySQLAdapter:
    is_aio_driver = True

    def process_sql(self, query_name, _op_type, sql):
        return utilities.sql_to_print_style(sql)

    async def select(self, conn, query_name, sql, parameters, record_class=None):
        async with conn.cursor(cursor=DictCursor) as cur:
            await cur.execute(sql, parameters)
            results = await cur.fetchall()
            if record_class is not None:
                column_names = [c.name for c in cur.description]
                results = [
                    record_class(**dict(zip(column_names, row))) for row in results
                ]
        return results

    async def select_one(self, conn, query_name, sql, parameters, record_class=None):
        async with conn.cursor(cursor=DictCursor) as cur:
            await cur.execute(sql, parameters)
            result = await cur.fetchone()
            if result is not None and record_class is not None:
                column_names = [c.name for c in cur.description]
                result = record_class(**dict(zip(column_names, result)))
        return result

    async def select_value(self, conn, query_name, sql, parameters):
        async with conn.cursor(cursor=DictCursor) as cur:
            await cur.execute(sql, parameters)
            result = await cur.fetchone()
        return result[0] if result else None

    @asynccontextmanager
    async def select_cursor(self, conn, query_name, sql, parameters):
        async with conn.cursor(cursor=DictCursor) as cur:
            await cur.execute(sql, parameters)
            yield cur

    async def insert_returning(self, conn, query_name, sql, parameters):
        async with conn.cursor(cursor=DictCursor) as cur:
            await cur.execute(sql, parameters)
            return cur.lastrowid

    async def insert_update_delete(self, conn, query_name, sql, parameters):
        async with conn.cursor(cursor=DictCursor) as cur:
            await cur.execute(sql, parameters)

    async def insert_update_delete_many(self, conn, query_name, sql, parameters):
        async with conn.cursor(cursor=DictCursor) as cur:
            await cur.execute(sql, parameters)

    @staticmethod
    async def execute_script(conn, sql):
        async with conn.cursor(cursor=DictCursor) as cur:
            await cur.execute(sql)

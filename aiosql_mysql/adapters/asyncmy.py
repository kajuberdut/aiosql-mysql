from collections import defaultdict
from contextlib2 import asynccontextmanager

import re


var_pattern = re.compile(
    r'(?P<dblquote>"[^"]+")|'
    r"(?P<quote>\'[^\']+\')|"
    r"(?P<lead>[^:]):(?P<var_name>[\w-]+)(?P<trail>[^:]?)"
)


class AsyncMySQLAdapter:
    is_aio_driver = True

    def process_sql(self, query_name, _op_type, sql):
        count = 0
        adj = 0

        for match in var_pattern.finditer(sql):
            gd = match.groupdict()
            # Do nothing if the match is found within quotes.
            if gd["dblquote"] is not None or gd["quote"] is not None:
                continue

            var_name = gd["var_name"]
            if var_name in self.var_sorted[query_name]:
                replacement = f"${self.var_sorted.index(query_name)+1}"
            else:
                replacement = f"${len(self.var_sorted[query_name])+1}"
                self.var_sorted[query_name].append(var_name)

            start = match.start() + len(gd["lead"]) + adj
            end = match.end() - len(gd["trail"]) + adj

            sql = sql[:start] + replacement + sql[end:]

            replacement_len = len(replacement)
            # the lead ":" char is the reason for the +1
            var_len = len(var_name) + 1
            if replacement_len < var_len:
                adj = adj + replacement_len - var_len
            else:
                adj = adj + var_len - replacement_len

        return sql

    def maybe_order_params(self, query_name, parameters):
        if isinstance(parameters, dict):
            return [parameters[rk] for rk in self.var_sorted[query_name]]
        elif isinstance(parameters, tuple):
            return parameters
        else:
            raise ValueError(f"Parameters expected to be dict or tuple, received {parameters}")

    async def select(self, conn, query_name, sql, parameters, record_class=None):
        parameters = self.maybe_order_params(query_name, parameters)
        async with MaybeAcquire(conn) as connection:
            results = await connection.fetch(sql, *parameters)
            if record_class is not None:
                results = [record_class(**dict(rec)) for rec in results]
        return results

    async def select_one(self, conn, query_name, sql, parameters, record_class=None):
        parameters = self.maybe_order_params(query_name, parameters)
        async with MaybeAcquire(conn) as connection:
            result = await connection.fetchrow(sql, *parameters)
            if result is not None and record_class is not None:
                result = record_class(**dict(result))
        return result

    async def select_value(self, conn, query_name, sql, parameters):
        parameters = self.maybe_order_params(query_name, parameters)
        async with MaybeAcquire(conn) as connection:
            return await connection.fetchval(sql, *parameters)

    @asynccontextmanager
    async def select_cursor(self, conn, query_name, sql, parameters):
        parameters = self.maybe_order_params(query_name, parameters)
        async with MaybeAcquire(conn) as connection:
            stmt = await connection.prepare(sql)
            async with connection.transaction():
                yield stmt.cursor(*parameters)

    async def insert_returning(self, conn, query_name, sql, parameters):
        parameters = self.maybe_order_params(query_name, parameters)
        async with MaybeAcquire(conn) as connection:
            res = await connection.fetchrow(sql, *parameters)
            if res:
                return res[0] if len(res) == 1 else res
            else:
                return None

    async def insert_update_delete(self, conn, query_name, sql, parameters):
        parameters = self.maybe_order_params(query_name, parameters)
        async with MaybeAcquire(conn) as connection:
            await connection.execute(sql, *parameters)

    async def insert_update_delete_many(self, conn, query_name, sql, parameters):
        parameters = [self.maybe_order_params(query_name, params) for params in parameters]
        async with MaybeAcquire(conn) as connection:
            await connection.executemany(sql, parameters)

    @staticmethod
    async def execute_script(conn, sql):
        async with MaybeAcquire(conn) as connection:
            return await connection.execute(sql)
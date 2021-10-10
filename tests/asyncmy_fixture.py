import asyncmy
import tenacity
from ward import Scope, fixture

from .docker_fixture import DATABASE, HOST, ROOT_USER, db, password, port


@fixture(scope=Scope.Module)
async def a_connection(port=port, password=password, db=db):
    @tenacity.retry(
        reraise=True,
        stop=tenacity.stop_after_delay(120),
        wait=tenacity.wait_fixed(3),
        retry=tenacity.retry_if_exception_type(asyncmy.errors.OperationalError),
    )
    async def get_connection():
        conn = await asyncmy.connect(
            host=HOST,
            port=port,
            user=ROOT_USER,
            password=password,
            db=DATABASE,
        )
        return conn

    conn = await get_connection()
    yield conn
    conn.close()


@fixture(scope=Scope.Test)
async def a_cursor(conn=a_connection):
    async with conn.cursor(cursor=asyncmy.cursors.DictCursor) as cursor:
        yield cursor

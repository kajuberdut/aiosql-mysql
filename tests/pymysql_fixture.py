import pymysql
import tenacity
from ward import Scope, fixture

from .docker_fixture import DATABASE, HOST, ROOT_USER, db, password, port

@fixture(scope=Scope.Module)
def b_connection(port=port, password=password, db=db):
    @tenacity.retry(
        reraise=True,
        stop=tenacity.stop_after_delay(120),
        wait=tenacity.wait_fixed(3),
        retry=tenacity.retry_if_exception_type(pymysql.err.OperationalError),
    )
    def get_connection():
        conn = pymysql.connect(
            host=HOST,
            port=port,
            user=ROOT_USER,
            password=password,
            database=DATABASE,
            cursorclass=pymysql.cursors.DictCursor,
        )
        return conn

    conn = get_connection()
    yield conn
    conn.close()


@fixture(scope=Scope.Test)
def b_cursor(conn=b_connection):
    with conn.cursor() as cursor:
        yield cursor

import random
import socket
import string

import asyncmy
import docker
import pymysql
import tenacity
from ward import Scope, fixture, test

DATABASE = "TestDatabase"
IMAGE = "mysql:latest"
HOST = "127.0.0.1"
PASSWORD_LENGTH = 12
PASSWORD_SET = (
    string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
)
ROOT_USER = "root"


@fixture(scope=Scope.Global)
def password():
    return "".join(
        random.sample(
            PASSWORD_SET,
            PASSWORD_LENGTH,
        )
    )


@fixture(scope=Scope.Global)
def port():
    """Find some open port on host."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port_value = s.getsockname()[1]
    s.close()
    return port_value


@fixture(scope=Scope.Global)
def db(port=port, password=password):
    """Create MySQL docker attached to port."""
    client = docker.from_env()
    container = client.containers.run(
        IMAGE,
        environment={
            "MYSQL_DATABASE": DATABASE,
            "MYSQL_ROOT_PASSWORD": password,
        },
        ports={"3306/tcp": (HOST, port)},
        detach=True,
        remove=True,
    )
    yield container
    container.stop()


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


@test("Async Connection Test")
async def _(cur=a_cursor):
    await cur.execute("SELECT 42 as thing;")
    result = await cur.fetchall()
    assert result[0]["thing"] == 42


@fixture(scope=Scope.Module)
def b_connection(port=port, password=password, db=db):
    @tenacity.retry(
        reraise=True,
        stop=tenacity.stop_after_delay(120),
        wait=tenacity.wait_fixed(3),
        retry=tenacity.retry_if_exception_type(asyncmy.errors.OperationalError),
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


@test("Blocking Connection Test")
def _(cur=b_cursor):
    cur.execute("SELECT 42 as thing;")
    result = cur.fetchall()
    assert result[0]["thing"] == 42

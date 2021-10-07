import random
import socket
import string

import asyncmy
import docker
import tenacity
from asyncmy import errors
from asyncmy.cursors import DictCursor
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
async def pool(port=port, password=password, db=db):
    @tenacity.retry(
        reraise=True,
        stop=tenacity.stop_after_delay(120),
        wait=tenacity.wait_fixed(3),
        retry=tenacity.retry_if_exception_type(errors.OperationalError),
    )
    async def get_pool():
        pool = await asyncmy.create_pool(
            host=HOST,
            port=port,
            user=ROOT_USER,
            password=password,
            db=DATABASE,
        )
        return pool

    pool = await get_pool()
    yield pool
    pool.close()


@fixture(scope=Scope.Module)
async def connection(pool=pool):
    async with pool.acquire() as conn:
        yield conn


@fixture(scope=Scope.Test)
async def cursor(conn=connection):
    async with conn.cursor(cursor=DictCursor) as cursor:
        yield cursor


@test("Connection Test")  # you can use markdown in these descriptions!
async def test_example(cur=cursor):

    await cur.execute("SELECT 42 as thing;")
    result = await cur.fetchall()
    assert result[0]["thing"] == 42

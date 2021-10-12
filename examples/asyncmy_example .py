from contextlib import contextmanager

import aiosql
import docker
import asyncmy
import tenacity
from aiosql_mysql import AsyncMySQLAdapter


@contextmanager
def get_docker():
    client = docker.from_env()
    container = client.containers.run(
        "mysql:latest",
        environment={
            "MYSQL_DATABASE": "ExampleDb",
            "MYSQL_ROOT_PASSWORD": "password",
        },
        ports={"3306/tcp": ("127.0.0.1", 3306)},
        detach=True,
        remove=True,
    )
    try:
        yield container
    finally:
        container.stop()


@tenacity.retry(
    reraise=True,
    stop=tenacity.stop_after_delay(60),
    wait=tenacity.wait_fixed(3),
)
async def get_connect():
    conn = await asyncmy.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="password",
        database="ExampleDb",
    )
    return conn

queries = aiosql.from_path("./users.sql", AsyncMySQLAdapter)

async def main():
    conn = await get_connect()

    await queries.create_users(conn)
    await queries.insert_user(conn,user_name='sbob', first_name='Bob', last_name='Smith')
    result = await queries.get_user_by_username(conn, username="sbob")
    print(result)


if __name__ == "__main__":
    import asyncio

    with get_docker() as container:
        asyncio.run(main())
    # {'userid': 1, 'username': 'sbob', 'firstname': 'Bob', 'lastname': 'Smith'}

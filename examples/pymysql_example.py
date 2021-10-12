from contextlib import contextmanager

import aiosql
import docker
import pymysql
import tenacity
from aiosql_mysql import PyMySQLAdaptor


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
    stop=tenacity.stop_after_delay(120),
    wait=tenacity.wait_fixed(3),
)
def get_connect():
    return pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="password",
        database="ExampleDb",
        cursorclass=pymysql.cursors.DictCursor,
    )


if __name__ == "__main__":
    with get_docker() as container:
        queries = aiosql.from_path("./users.sql", PyMySQLAdaptor)
        conn = get_connect()
        
        queries.create_users(conn)
        queries.insert_user(conn,user_name='sbob', first_name='Bob', last_name='Smith')
        result = queries.get_user_by_username(conn, username="sbob")
        print(result)
    # {'userid': 1, 'username': 'bob', 'firstname': 'bob', 'lastname': 'smith'}

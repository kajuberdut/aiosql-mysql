from re import S
import aiosql
from ward import test, fixture

from .pymysql_fixture import b_cursor, b_connection
from aiosql_mysql import PyMySQLAdaptor


@fixture()
def sql():
    return """
-- name: select-one^
SELECT 1 as one;

-- name: select-one-two
SELECT 1 as column1
UNION
SELECT 2 as column1;

-- name: select-one-where-one-equals^
SELECT 1 as one
WHERE :one = 1;
"""


@fixture
def queries_from_str(sql=sql):
    return aiosql.from_str(sql, PyMySQLAdaptor)


@test("Blocking Connection Test", tags=["pymysql", "connection", "blocking"])
def _(cur=b_cursor):
    cur.execute("SELECT 42 as thing;")
    result = cur.fetchall()
    assert result[0]["thing"] == 42


@test("Test select", tags=["pymysql", "aiosql", "select", "blocking"])
def _(conn=b_connection, queries=queries_from_str):
    one_two = queries.select_one_two(conn)
    assert one_two[0]["column1"] == 1
    assert one_two[1]["column1"] == 2


@test("Test select one", tags=["pymysql", "aiosql", "select", "select one", "blocking"])
def _(conn=b_connection, queries=queries_from_str):
    one = queries.select_one(conn)
    assert one["one"] == 1


@test(
    "Test select where :one = 1",
    tags=["pymysql", "aiosql", "select", "select one", "where", "blocking"],
)
def _(conn=b_connection, queries=queries_from_str):
    one = queries.select_one_where_one_equals(conn, one=1)
    assert one["one"] == 1


@test(
    "Test select where :one != 1",
    tags=["pymysql", "aiosql", "select", "select one", "where", "blocking"],
)
def _(conn=b_connection, queries=queries_from_str):
    one = queries.select_one_where_one_equals(conn, one=2)
    assert one is None

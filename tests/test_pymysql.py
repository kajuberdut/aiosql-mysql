from ward import test

from .pymysql_fixture import b_cursor


@test("Blocking Connection Test")
def _(cur=b_cursor):
    cur.execute("SELECT 42 as thing;")
    result = cur.fetchall()
    assert result[0]["thing"] == 42

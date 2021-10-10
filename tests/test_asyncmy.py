from ward import test

from .asyncmy_fixture import a_cursor


@test("Async Connection Test")
async def _(cur=a_cursor):
    await cur.execute("SELECT 42 as thing;")
    result = await cur.fetchall()
    assert result[0]["thing"] == 42

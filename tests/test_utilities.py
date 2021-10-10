from aiosql_mysql import utilities
from ward import test

@test("Test variable replacement")
def _():
    assert utilities.sql_to_print_style(text="SELECT 1 WHERE :thing = 1") == "SELECT 1 WHERE %(thing)s = 1"

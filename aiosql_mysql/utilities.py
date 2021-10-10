import re

# looking for : without a \ escaping it
# followed by any number of letters, numbers or "_", "-"" characters.
variables = re.compile(r"""[^\\](:[\w\d_-]*)""")

def sql_to_print_style(text: str) -> str:
    """ Convert the aiosql style :variable to print format style %(variable)s
    """
    return variables.sub(
        lambda m: f"{m.group(0)[:1]}%({m.group(1)[1:]})s", text
    )

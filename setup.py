import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name="aiosql_mysql",
    version="0.0.1",
    author="Patrick Shechet",
    author_email="patrick.shechet@gmail.com",
    description=("A MySQL driver adaptor for aiosql"),
    license="MIT",
    packages=find_packages(),
    long_description=README,
    long_description_content_type="text/markdown",
    extras_require={"pymysql": ["pymysql[rsa]"], "asyncmy": ["asyncmy"]},
    url="https://github.com/kajuberdut/aiosql-mysql",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3 :: Only",
    ],
)

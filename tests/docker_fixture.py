import random
import socket
import string

import docker
from ward import Scope, fixture


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

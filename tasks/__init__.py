from invoke import Collection

from . import (
    cli,
    docker,
)

ns = Collection(
    cli,
    docker,
)

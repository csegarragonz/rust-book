from invoke import task
from os import environ
from subprocess import run
from tasks.env import PROJ_ROOT


@task(default=True)
def cli(ctx, service="cli", clean=False):
    """
    Get a shell into the development container
    """
    build_env = environ.copy()
    docker_cmd = "docker compose up -d --no-recreate"
    run(docker_cmd, shell=True, check=True, cwd=PROJ_ROOT, env=build_env)

    docker_cmd = "docker compose exec -it {} bash".format(service)
    run(docker_cmd, shell=True, check=True, cwd=PROJ_ROOT, env=build_env)


@task()
def stop(ctx):
    build_env = environ.copy()
    run(
        "docker compose down",
        shell=True,
        check=True,
        cwd=PROJ_ROOT,
        env=build_env,
    )

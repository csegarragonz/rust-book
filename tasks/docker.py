from invoke import task
from os.path import join
from subprocess import run
from tasks.env import PROJ_ROOT

IMAGE_NAME = "rust-book"


def get_version():
    ver_file = join(PROJ_ROOT, "VERSION")

    with open(ver_file, "r") as fh:
        version = fh.read()

    version = version.strip()
    return version


def _get_docker_tag():
    ver = get_version()
    return "csegarragonz/{}:{}".format(IMAGE_NAME, ver)


def _do_container_build(nocache=False, push=False):
    tag_name = _get_docker_tag()
    # ver = get_version()

    if nocache:
        no_cache_str = "--no-cache"
    else:
        no_cache_str = ""

    dockerfile = join(PROJ_ROOT, "Dockerfile")

    build_cmd = [
        "docker build",
        no_cache_str,
        "-t {}".format(tag_name),
        "-f {}".format(dockerfile),
        # "--build-arg RUST_VERSION={}".format(ver),
        ".",
    ]
    build_cmd = " ".join(build_cmd)

    print(build_cmd)
    run(build_cmd, shell=True, check=True, env={"DOCKER_BUILDKIT": "1"})

    if push:
        _do_push()


def _do_push():
    tag_name = _get_docker_tag()

    cmd = "docker push {}".format(tag_name)
    print(cmd)
    run(cmd, shell=True, check=True)


@task()
def build(ctx, nocache=False, push=False):
    """
    Build containers for faabric. Targets are: `faabric`, and `faabric-base`
    """
    _do_container_build(nocache=nocache, push=push)


@task()
def push(ctx):
    """
    Push containers for faabric. Targets are: `faabric`, and `faabric-base`
    """
    _do_push()

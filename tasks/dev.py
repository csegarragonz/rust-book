from copy import copy
from invoke import task
from os import environ
from os.path import exists, join
from shutil import rmtree
from subprocess import run
from sys import exit
from tasks.env import (
    PROJ_ROOT,
)


@task
def format(ctx, check=False):
    """
    Format Go and Python code
    """
    # Include shell environment for out-of-tree builds to find the right go
    # binary
    shell_env = copy(environ)

    if check:
        go_cmd = 'gofmt -l $(find . -type f -name "*.go")'
        py_cmd_black = (
            "python3 -m black --check $(find . -type f -name "
            '"*.py" -not -path "./venv/*" -not -path "./venv-bm/*")'
        )
        py_cmd_flake = (
            "python3 -m flake8 --count $(find . -type f -name "
            '"*.py" -not -path "./venv/*" -not -path "./venv-bm/*")'
        )
    else:
        go_cmd = 'gofmt -w $(find . -type f -name "*.go")'
        py_cmd_black = (
            'python3 -m black $(find . -type f -name "*.py" -not '
            '-path "./venv/*" -not -path "./venv-bm/*")'
        )
        py_cmd_flake = (
            "python3 -m flake8 --exit-zero $(find . -type f -name "
            '"*.py" -not -path "./venv/*" -not -path "./venv-bm/*")'
        )

    # Run Go formatting
    print(go_cmd)
    result = run(
        go_cmd,
        shell=True,
        check=True,
        cwd=PROJ_ROOT,
        capture_output=True,
        env=shell_env,
    )
    if check and result.stdout:
        print("Found errors checking Go formatting: {}".format(result.stdout))
        exit(1)

    # Run Python formatting. Note that running with the --check flag already
    # returns an error code if code is not adequately formatted
    print(py_cmd_black)
    run(py_cmd_black, shell=True, check=True, cwd=PROJ_ROOT)
    # Same for flake8's --count flag
    print(py_cmd_flake)
    run(py_cmd_flake, shell=True, check=True, cwd=PROJ_ROOT)

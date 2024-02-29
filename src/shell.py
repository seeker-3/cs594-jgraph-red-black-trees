from subprocess import run


def bash(command: str) -> None:
    run(
        command,
        shell=True,
        check=True,
        executable="/bin/bash",
    ).check_returncode()

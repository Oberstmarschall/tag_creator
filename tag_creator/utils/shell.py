import subprocess
from tag_creator.logger import logger
from typing import Any


def exec(command: str, *args: tuple[str, ...], **kwargs: Any) -> str:
    """Execute shell command

    Args:
        command (str): cmd to execute.

    Returns:
        str: command stdout
    """
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, encoding="UTF-8", *args, **kwargs  # type: ignore
        )
        return str(result.stdout)
    except subprocess.CalledProcessError as ex:
        logger.error(f"Execution failed. Status code: {ex.returncode}. Message: {ex.stderr}")
        raise

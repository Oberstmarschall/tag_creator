import subprocess
from tag_creator.logger import logger


def exec(command, *args, **kwargs):
    try:
        return subprocess.run(
            command, shell=True, check=True, capture_output=True, encoding="UTF-8", *args, **kwargs
        )
    except subprocess.CalledProcessError as ex:
        logger.error(f"Execution failed. Status code: {ex.returncode}. Message: {ex.stderr}")
        raise

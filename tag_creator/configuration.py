import yaml
import os
from typing import Dict, List, Any
from tag_creator.arguments import args
from tag_creator.logger import logger

CONFIGURATION: Dict[str, str] = {}


def read_configuration() -> Dict[str, Any]:
    global CONFIGURATION
    if not CONFIGURATION:
        with open(f"{os.path.dirname(__file__)}/configuration.yml", "r") as f:
            CONFIGURATION = yaml.safe_load(f)
            CONFIGURATION.update(custom_config())
    return CONFIGURATION


def custom_config() -> Dict[str, Any]:
    if os.path.exists(os.path.abspath(args.config)) and args.config:
        with open(args.config, "r") as f:
            logger.info("Custom config read!")
            return dict(yaml.safe_load(f))
    return {}


def allowed_commit_types() -> List[str]:
    cfg = read_configuration()
    return list(cfg["commit_types"])

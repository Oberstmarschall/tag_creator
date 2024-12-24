import yaml
import os

CONFIGURATION = {}

def read_configuration():
    global CONFIGURATION
    if not CONFIGURATION:
        with open(f"{os.path.dirname(__file__)}/configuration.yml", "r") as f:
            CONFIGURATION = yaml.safe_load(f)
    return CONFIGURATION

def allowed_commit_types():
    cfg = read_configuration()
    return cfg["commit_types"]

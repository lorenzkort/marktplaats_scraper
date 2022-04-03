"""
* Reads config file and validates datatypes
* Creates basic variables needed for the project
"""

from pathlib import Path
from typing import Dict, List, Sequence, Optional, Union

from pydantic import BaseModel
from strictyaml import YAML, load

import jobs

# Project Directories
PACKAGE_ROOT = Path(jobs.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config/config.yml"
DATASET_DIR = PACKAGE_ROOT / "datasets"
LOG_DIR = ROOT / "logs"
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

class Search(BaseModel):
    """
    Search on marktplaats
    """
    keyword: str
    categoryId: int
    titleAndDescription: bool

class Channel(BaseModel):
    """
    Telegram channel destination
    """
    chatId: int
    postalcode: str
    spam_sellers: list[str]
    searches: list[Search]

class Config(BaseModel):
    """
    Master config object.
    """
    package_name: str
    runs_per_hour: int
    channels: list[Channel]

    log_format: str
    date_time_format: str

def find_config_file() -> Path:
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:
    """Parse YAML containing the package configuration."""
    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(**parsed_config.data)
    
    return _config

config = create_and_validate_config()
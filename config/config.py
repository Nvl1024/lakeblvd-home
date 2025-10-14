"""
from config import config_name
"""
import os
import configparser


def section(field_name: str) -> configparser.SectionProxy:
    """
    get section of the configuration
    """
    # check config file
    config_file = os.path.join(__file__, '..', 'lakeblvd.config')
    config_file = os.path.normpath(config_file)
    if not os.path.isfile(config_file):
        raise FileNotFoundError(f"Config not found: {config_file}")
    # start config parser instance
    cp = configparser.ConfigParser()
    cp.read(config_file)
    section_proxy = cp[field_name]
    return section_proxy

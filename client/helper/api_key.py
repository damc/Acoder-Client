from os import environ

from .files import write, content


def save_api_key(api_key: str):
    """Save api key"""
    write(file_path(), api_key)


def load_api_key() -> str:
    """Load api key"""
    api_key_file = file_path()
    return content(api_key_file)


def file_path() -> str:
    """Get API Key file path"""
    home_directory = environ['HOME']
    return f"{home_directory}/.acoder/api_key"

from appdirs import user_data_dir

from .files import write, content


def save_api_key(api_key: str):
    """Save api key"""
    write(file_path(), api_key)


class APIKeyMissing(Exception):
    pass


def load_api_key() -> str:
    """Load api key"""
    api_key_file = file_path()
    try:
        return content(api_key_file)
    except FileNotFoundError:
        raise APIKeyMissing("API key missing")


APP_NAME = APP_AUTHOR = 'Acoder'


def file_path() -> str:
    """Get API Key file path"""
    return f"{user_data_dir(APP_NAME, APP_AUTHOR)}/api_key"

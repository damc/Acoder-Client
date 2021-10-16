from click import command, argument, echo

from ..helper.api_key import save_api_key, file_path


@command()
@argument("api_key")
def configure(api_key: str):
    """Provide API key for authentication

    \b
    Args:
        api_key(str): API key for authentication
    """
    save_api_key(api_key)
    echo(f'The API key has been saved to the file: "{file_path()}".')


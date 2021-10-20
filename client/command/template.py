from click import command, argument, echo

from ..config import config
from ..helper.files import content, write


@command()
@argument("file_path", default="task.md")
def template(file_path: str):
    """Generate template file for task description

    \b
    Args:
        file_path(str): Path to task file
    """
    content_ = content(config['BASE_PATH'] + "client/templates/standard.md")
    write(file_path, content_)
    echo(f"The template file has been generated in: {file_path}.")

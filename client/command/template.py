from click import command, argument, echo

from ..helper.files import content, write


@command()
@argument("file_path", default="task.md")
def template(file_path: str):
    """Generate template file for task description

    \b
    Args:
        file_path(str): Path to task file
    """
    write(file_path, content("client/templates/standard.md"))
    echo(f"The template file has been generated in: {file_path}.")

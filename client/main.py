from click import group, version_option
from logging import basicConfig

from .command.configure import configure
from .command.solve import solve
from .command.template import template
from .config import config


if config['LOGGING_LEVEL']:
    basicConfig(filename='logs.log', level=config['LOGGING_LEVEL'])


@group()
@version_option("1.0", prog_name="Acoder")
def main():
    """Generate code to accomplish a task (using AI).

    \b
    Usage:
    1. Sign up on the Acoder website.
    2. After signing in, in the "Dashboard", you can see you API key.
    3. Run `acoder configure <your API key here>`.
    4. Go to your project directory.
    5. Run `acoder template`. It will generate `task.md` file.
    6. Open the `task.md` file.
    7. Change the `task.md` according to the instruction in it.
    8. Run `acoder solve` and follow the instructions.
    9. (Optional) Add `task.md` file to `.gitignore`.

    When using Acoder the next time, you need to execute only the steps
    from 6 to 8 - it's not necessary to configure Acoder and regenerate
    the template each time you want to solve a task.

    We recommend to never delete `task.md` file. Instead, when you want
    to solve a different task, simply change the content of task.md
    file and then run `acoder solve`.

    You can run any command with --help to get more help on how to
    use the command (e.g. `acoder solve --help`).
    """
    pass


main.add_command(solve)
main.add_command(template)
main.add_command(configure)

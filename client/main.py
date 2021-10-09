from click import group, version_option
from logging import basicConfig, DEBUG

from .command.configure import configure
from .command.solve import solve
from .command.template import template


basicConfig(filename='logs.log', level=DEBUG)


@group()
@version_option("1.0", prog_name="Acoder")
def main():
    pass


main.add_command(solve)
main.add_command(template)
main.add_command(configure)

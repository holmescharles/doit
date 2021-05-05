import click

from . import bib
from . import text

COMMANDS = {
    "bib": bib.main,
    "text": text.main,
    }


@click.group()
def main():
    ...


for name, func in COMMANDS.items():
    main.add_command(func, name=name)

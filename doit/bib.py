import re

from bibtexparser import loads
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.customization import author, splitname
import click
import requests


NOT_ALPHANUM = re.compile("[^a-zA-Z0-9]")
SMALL_WORDS = re.compile(
    r"^(a|an|and|as|at|but|by|en|for|if|in|of|on|or|the|to|v\.?|via|vs\.?)$"
    )


@click.command()
@click.argument("dois", nargs=-1)
def main(dois):
    text = "\n".join(fetch_bib(x) for x in dois)
    click.echo(to_string(from_string(text)))


def fetch_bib(doi):
    return requests.get(
        "https://doi.org/" + doi,
        headers={"Accept": "application/x-bibtex"},
        ).text


def from_string(text):
    parser = BibTexParser()
    parser.customization = custom_identifier
    return loads(text, parser=parser)


def to_string(bib):
    writer = BibTexWriter()
    writer.indent = "  "
    writer.display_order = ["author", "title", "year", "journal"]
    return writer.write(bib)


def custom_identifier(record):
    record["ID"] = author_name(record) + year(record) + title_word(record)
    return record


def author_name(record):
    record = record.copy()
    author(record)
    lastname = splitname(record["author"][0])["last"][0]
    return NOT_ALPHANUM.split(lastname)[0].lower()


def year(record):
    return record["year"]


def title_word(record):
    return next(
        x for x in NOT_ALPHANUM.split(record["title"].lower())
        if not SMALL_WORDS.match(x)
        ).lower()


if __name__ == "__main__":
    main()

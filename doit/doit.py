import os
from pathlib import Path
import re

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import click
import habanero

NOT_ALPHANUM = re.compile('[^a-zA-Z0-9]')
SMALL_WORDS = re.compile(
    r"^(a|an|and|as|at|but|by|en|for|if|in|of|on|or|the|to|v\.?|via|vs\.?)$"
    )

class Work:

    def __init__(self, doi):
        self.doi = doi

    def text(self):
        return habanero.cn.content_negotiation(ids=self.doi, format = "text")

    def bib(self):
        text = habanero.cn.content_negotiation(ids=self.doi)
        parser = BibTexParser()
        parser.customization = self.__class__.custom_id
        db =  bibtexparser.loads(text, parser=parser)
        self.__class__.report_duplicate_ids(db.entries[0])
        writer = BibTexWriter()
        writer.indent = "  "
        writer.display_order = ["author", "title", "year", "journal"]
        return writer.write(db)

    @staticmethod
    def custom_id(record):
        record_ = record.copy()
        bibtexparser.customization.author(record_)
        nameparts = bibtexparser.customization.splitname(record_["author"][0])
        lastname = nameparts["last"]
        assert len(lastname) == 1
        lastname = NOT_ALPHANUM.split(lastname[0])[0].lower()
        titleword = next(
            x for x in NOT_ALPHANUM.split(record["title"])
            if not SMALL_WORDS.match(x)
            ).lower()
        record["ID"] = lastname + record["year"] + titleword
        return record

    @staticmethod
    def report_duplicate_ids(record):
        ids = fetch_all_entries_by_id()
        if record["ID"] in ids:
            click.echo(f"This ID [{record['ID']}] already in:", err=True)
            for entry in ids[record["ID"]]:
                click.echo(f" - {entry['FILE']}", err=True)
            click.echo(err=True)



@click.group()
def main():
    verify_one_doi_per_id()


@main.command()
@click.argument('doi')
def bib(doi):
    click.echo(Work(doi).bib(), nl=False)


@main.command()
@click.argument('doi')
def text(doi):
    click.echo(Work(doi).text(), nl=False)


def verify_one_doi_per_id():
    for id_, entries in fetch_all_entries_by_id().items():
        if len(set(x["doi"] for x in entries)) > 1:
            click.echo(f"WARNING: {id_} has multiple dois.", err=True)
            for entry in entries:
                click.echo(f" - {entry['doi']}")


def fetch_all_entries_by_id():
    if "BIBS" not in os.environ:
        return []
    bibs = Path(os.environ["BIBS"]).glob("**/*.bib")
    ids = {}
    for bib in bibs:
        with bib.open() as infile:
            db = bibtexparser.load(infile)
            for entry in db.entries:
                if not entry["ID"] in ids:
                    ids[entry["ID"]] = []
                entry["FILE"] = bib
                ids[entry["ID"]].append(entry)
    return ids


if __name__ == "__main__":
    main()

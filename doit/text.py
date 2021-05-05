import click
import requests

URL = "https://doi.org/"

HEADERS = {
    "Accept": "text/x-bibliography; style=apa",
}


@click.command()
@click.argument("dois", nargs=-1)
def main(dois):
    text = "\n".join(fetch_citation(x) for x in dois)
    click.echo(text)


def fetch_citation(doi):
    return requests.get(
        "https://doi.org/" + doi,
        headers={"Accept": "text/x-bibliography; style=apa"}
        ).text

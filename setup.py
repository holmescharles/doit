import setuptools

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="doit",
    version="0.1",
    description="Convert DOI to a bibtex entry.",
    long_description=long_description,
    long_description_context_type="text/markdown",
    author="Charles D. Holmes",
    author_email="holmes@wustl.edu",
    url="https://github.com/holmescharles/doit",
    packages=setuptools.find_packages(),
    install_require=[
        "click",
        "requests",
        "bibtexparser",
        ],
    entry_points={"console_scripts": ["doit = doit:main"]},
    )

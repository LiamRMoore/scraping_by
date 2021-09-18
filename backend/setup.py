import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="scrapying_by",
    description="Web scraping utilities for identifying contracts",
    author="Liam R. Moore",
    packages=find_packages(exclude=["data", "figures", "output", "notebooks"]),
    long_description="TODO",  # read("README.md"),
)

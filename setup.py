import io
from setuptools import setup, find_packages

requirements = ["bs4", "dateparser", "autotui"]

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fo:
    long_description = fo.read()

setup(
    name="old_forums",
    version="0.1.0",
    url="https://github.com/seanbreckenridge/old_forums",
    author="Sean Breckenridge",
    author_email="seanbrecke@gmail.com",
    description=("""Parses posts/achievements from random forums I used in the past"""),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    packages=find_packages(include=["old_forums"]),
    install_requires=requirements,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)

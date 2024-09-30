"""
File containing the required information to successfully build a python package
"""

import setuptools

with open("README.md", "r", encoding="utf-8", newline="\n") as fh:
    long_description = fh.read()
    
with open("requirements.txt", "r", encoding="utf-8", newline="\n") as fd:
    requirements = fd.read()

setuptools.setup(
    name='ContOpsSync',
    version='1.0.0',
    packages=setuptools.find_packages(),
    install_requires=requirements.split("\n"),
    author="Henry Letellier",
    author_email="henrysoftwarehouse@protonmail.com",
    description="This is a program that will allow you to run pre-set functions for managins instances like docker, docker compose, kubernetes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hanra-s-work/ContOpsSync",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

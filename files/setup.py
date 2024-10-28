"""
File containing the required information to successfully build a python package
"""

import setuptools

with open("README.md", "r", encoding="utf-8", newline="\n") as fh:
    long_description = fh.read()

setuptools.setup(
    name='cont-ops-sync',
    version='1.0.0',
    packages=setuptools.find_packages(),
    install_requires=[
        "colorama == 0.4.6",
        "prettytable ==3.11.0",
        "requests ==2.32.3",
        "tqdm ==4.66.6",
        "elevate == 0.1.3",
        "ask-question ==1.2.8",
        "colourise-output ==1.1.6",
        "display-tty ==1.1.7",
        "tty-ov ==1.0.47",
        "psutil ==6.1.0",
        "uuid == 1.30",
        "pytest ==8.3.3",
        "asciimatics_overlay_ov ==1.0.10",
        "english-words == 2.0.1",
        "pyinstaller ==6.11.0"

    ],
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

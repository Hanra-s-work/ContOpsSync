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
        "prettytable == 3.9.0",
        "requests ==2.32.2",
        "tqdm ==4.66.3",
        "elevate == 0.1.3",
        "ask-question ==1.2.8",
        "colourise-output == 1.1.3",
        "display-tty == 1.0.1",
        "tty-ov == 1.0.18",
        "psutil == 5.9.5",
        "uuid == 1.30",
        "pytest == 7.4.2",
        "asciimatics_overlay_ov ==1.0.10",
        "english-words == 2.0.1",
        "pyinstaller == 6.10.0"

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

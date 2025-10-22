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
        "requests ==2.32.4",
        "tqdm ==4.67.1",
        "display-tty ==1.1.12",
        "tty-ov ==1.0.75",
        "pytest ==8.3.5",
        "asciimatics_overlay_ov ==1.0.10",
        "english-words ==2.0.2",
        "pyinstaller ==6.12.0"

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

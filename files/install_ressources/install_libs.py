import os
import sys
import shutil
from platform import system
from urllib.request import urlretrieve

SUCCESS = 0
ERROR = 84


def download_file(url: str = "", filename: str = "") -> int:
    """ Download a file from a url """
    print(f"Downloading '{filename}'")
    if url == "":
        return ERROR
    if filename == "":
        return ERROR
    try:
        urlretrieve(url, filename)
        return SUCCESS
    except:
        return ERROR


def create_folder(fold_name: str = "") -> int:
    """ Create a folder """
    print(f"Creating folder: '{fold_name}'")
    if fold_name == "":
        return ERROR
    try:
        os.makedirs(fold_name, exist_ok=True)
        return SUCCESS
    except OSError:
        return ERROR


def remove_if_exists(filepath: str = "") -> int:
    """ Remove a file if it exists """
    print(f"Removing: '{filepath}'")
    if filepath == "":
        return ERROR
    try:
        os.remove(filepath)
        return SUCCESS
    except shutil.Error as err:
        print(f"Error: {err}")
        return ERROR


def create_environement(usr_system: str = "", environement_name: str = "") -> int:
    """ Create the python environement """
    print("Creating environment")
    if usr_system == "" or environement_name == "":
        return ERROR
    if usr_system == "Linux" or usr_system == "Java":
        return os.system(f"python3 -m venv {environement_name}")
    if usr_system == "Windows":
        return os.system(f"py -m venv {environement_name}")
    return ERROR


def activate_and_install_local_package(environement_name: str = "", package_path: str = "") -> int:
    """ Activate environement and install package """
    print(f"Installing local pip package '{package_path}'")
    if environement_name == "" or package_path == "":
        return ERROR
    if system() == "Linux" or system() == "Java":
        return os.system(f". ./{environement_name}/bin/activate && pip install {package_path} && deactivate")
    if system() == "Windows":
        return os.system(f".\\{environement_name}\\Scripts\\activate && pip install {package_path} && deactivate")
    return ERROR


def activate_and_install_requirement_package(environement_name: str = "") -> int:
    """ Activate environement and install package """
    print("Installing pip requirements")
    if environement_name == "":
        return ERROR
    if os.path.isfile("requirements.txt") is False:
        return SUCCESS
    if system() == "Linux" or system() == "Java":
        return os.system(f". ./{environement_name}/bin/activate && pip install -r requirements.txt && deactivate")
    if system() == "Windows":
        return os.system(f".\\{environement_name}\\Scripts\\activate && pip install -r requirements.txt && deactivate")
    return ERROR


CURRENT_SYSTEM = system()
TTY_LINK = "https://github.com/Hanra-s-work/tty_ov/archive/refs/tags/v1.0.4.tar.gz"
ASK_QUESTION_LINK = "https://github.com/Hanra-s-work/ask_question/archive/refs/tags/v1.2.0.tar.gz"
COLOURISE_OUTPUT_LINK = "https://github.com/Hanra-s-work/colourise_output/archive/refs/tags/v1.1.1.tar.gz"
DISP_OUTPUT_LINK = "https://github.com/Hanra-s-work/disp/releases/download/pre-v1.0.0/rdisp-1.0.0.tar.gz"
ENVIRONEMENT_NAME = "lenv"
LOCATION_FOLDER = f"{os.getcwd()}/libs"
TTY_OUTPUT_NAME = f"{LOCATION_FOLDER}/tty_ov.tar.gz"
ASK_QUESTION_OUTPUT_NAME = f"{LOCATION_FOLDER}/ask_question.tar.gz"
COLOURISE_OUTPUT_OUTPUT_NAME = f"{LOCATION_FOLDER}/colourise_output.tar.gz"
DISP_OUTPUT_NAME = f"{LOCATION_FOLDER}/disp.tar.gz"

if system() == "Windows":
    ENVIRONEMENT_NAME = "wenv"
if system() == "Java":
    ENVIRONEMENT_NAME = "menv"

if create_environement(CURRENT_SYSTEM, ENVIRONEMENT_NAME) != SUCCESS:
    print("Failed to create the python environement.")
    sys.exit(ERROR)

if create_folder(LOCATION_FOLDER) != SUCCESS:
    print("Failed to create the libs folder.")
    sys.exit(ERROR)

if download_file(DISP_OUTPUT_LINK, DISP_OUTPUT_NAME) != SUCCESS:
    print("Failed to download the disp library.")
    sys.exit(ERROR)

if download_file(TTY_LINK, TTY_OUTPUT_NAME) != SUCCESS:
    print("Failed to download the tty_ov library.")
    sys.exit(ERROR)

if download_file(ASK_QUESTION_LINK, ASK_QUESTION_OUTPUT_NAME) != SUCCESS:
    print("Failed to download the ask_question library.")
    sys.exit(ERROR)

if download_file(COLOURISE_OUTPUT_LINK, COLOURISE_OUTPUT_OUTPUT_NAME) != SUCCESS:
    print("Failed to download the colourise_output library.")
    sys.exit(ERROR)

if activate_and_install_requirement_package(ENVIRONEMENT_NAME) != SUCCESS:
    print("Failed to install the requirements.txt library.")
    sys.exit(ERROR)

if activate_and_install_local_package(ENVIRONEMENT_NAME, ASK_QUESTION_OUTPUT_NAME) != SUCCESS:
    print("Failed to install the ask_question library.")
    sys.exit(ERROR)

if activate_and_install_local_package(ENVIRONEMENT_NAME, COLOURISE_OUTPUT_OUTPUT_NAME) != SUCCESS:
    print("Failed to install the colourise_output library.")
    sys.exit(ERROR)

if activate_and_install_local_package(ENVIRONEMENT_NAME, TTY_OUTPUT_NAME) != SUCCESS:
    print("Failed to install the tty_ov library.")
    sys.exit(ERROR)

if activate_and_install_local_package(ENVIRONEMENT_NAME, DISP_OUTPUT_NAME) != SUCCESS:
    print("Failed to install the disp library.")
    sys.exit(ERROR)

print("Cleaning install packages")
if remove_if_exists(TTY_OUTPUT_NAME) != SUCCESS:
    print(
        f"Failed to delete the file: {TTY_OUTPUT_NAME}\nThe program will still work without any problem.")
    sys.exit(ERROR)
if remove_if_exists(ASK_QUESTION_OUTPUT_NAME) != SUCCESS:
    print(
        f"Failed to delete the file: {ASK_QUESTION_OUTPUT_NAME}\nThe program will still work without any problem.")
    sys.exit(ERROR)
if remove_if_exists(COLOURISE_OUTPUT_OUTPUT_NAME) != SUCCESS:
    print(
        f"Failed to delete the file: {COLOURISE_OUTPUT_OUTPUT_NAME}\nThe program will still work without any problem.")
    sys.exit(ERROR)

if remove_if_exists(DISP_OUTPUT_NAME) != SUCCESS:
    print(
        f"Failed to delete the file: {DISP_OUTPUT_NAME}\nThe program will still work without any problem.")
    sys.exit(ERROR)

print("Requirements, successfully installed, this script is not required anymore.")

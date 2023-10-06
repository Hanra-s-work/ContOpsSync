# tools

## Requirements

### Windows

    An internet connection
    Python installed

### Linux && Mac

    An internet connection
    Python installed
    The standard linux bash utilities (i.e. sudo, tr)

### Raspberry pi

If you have never run the script before, it is recommended to run `chmod +x ./raspberry_tools.sh` to make sure the current user has the right to run the script

For people running systems like rasberry pi (apt based systems) please run the tool `./raspberry_tools.sh`
Again, for the initial run it is recommended to run it with `sudo ./raspberry_tools.sh`
The end result should still be the program running

## Disclaimer

    for technical reasons this program isn't considered headless
    for sudo management, (required for linux and mac during initial installations):
        If you wish to not be prompted for a password:
            start the program with `sudo ./tools.sh`
            instead of the usual `./tools.sh`

## Start the program

If on windows:
    start the `tools.bat`

If on linux or Mac:
    On first launch:
        `chmod +x ./tools.sh && ./tools.sh`
    Otherwise:
        `./tools.sh`

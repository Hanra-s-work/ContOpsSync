# ContOpsSync

[![Static Badge](https://img.shields.io/badge/Buy_me_a_tea-Hanra-%235F7FFF?style=flat-square&logo=buymeacoffee&label=Buy%20me%20a%20coffee&labelColor=%235F7FFF&color=%23FFDD00&link=https%3A%2F%2Fwww.buymeacoffee.com%2Fhanra)](https://www.buymeacoffee.com/hanra)

ContOpsSync is a small Python utility to automate installation of Docker, Docker Compose, and Kubernetes-related tools across platforms.

## Status

Not actively developed; receives periodic dependency updates to keep it runnable on modern Python versions.

This program and most of the libraries have been written over 3/4 years ago, meaning that my way of coding has changed and even though I can maintain it I don't structure code the exact same way.

This repository might seem messy and this is because there was a lot of learning during the development, this was wether I was trying to install kubernetes, learning how to use asciimatics (didn't have the time to finish the ui, might one day finish the `asciimatics-overlay-ov` [https://pypi.org/project/asciimatics-overlay-ov/](https://pypi.org/project/asciimatics-overlay-ov/) but chances are slim.)

This program is very verbose, meaning that it tels every system command it runs and this is by design in the tty_ov module, this is so that the user has full transparency on what the program is doing. It is also very explicit about when a command succeeded or failed.

Anyway, I hope this project will help you in your research and ultimately save you time.

## Platforms

Primary support for Linux and Windows. macOS support is limited; some Raspberry Pi (ARM) support exists in the repo.

## What it does

- **Auto-detects your system:** Runs the appropriate install script when available.
- **Installs:** Docker, Docker Compose, and several Kubernetes-related tools via bundled scripts.
- **Pipe / stdin support:** The program accepts piped input (stdin) and treats it the same as text typed in the interactive TTY — you can pipe commands or input into the helper where supported. This behavior is provided by the `tty_ov` helper module (see the project page below).

## Notes

- Some installers and platform-specific scripts are incomplete.
- Installer scripts reference official product pages where possible; behavior depends on those external sources.
- The project uses the small helper module `tty_ov` to simplify cross-platform system calls.
- For more details on terminal behaviour, prompts and piped input support see the `tty_ov` project: [https://pypi.org/project/tty-ov/](https://pypi.org/project/tty-ov/)

## Quick start

- (Optional) Create a virtual environment and install dependencies listed under `files`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r files/requirements.txt
```

- Run the program from the repository root while keeping the environement active (interactive):

```bash
python files/src/main.py
```

- Command-line flags:

```bash
-nc, --no-colour    Disable coloured output
```

## Platform entrypoints

### Windows

- Use the `RUN_ME.bat` wrapper from the repository root. It calls `files\\tools.bat`, which presents the interactive tools and installers.
- To run with elevated privileges (required for some installers), right-click `RUN_ME.bat` and choose "Run as administrator". This is optional — the program will prompt for UAC elevation when an action needs it. Running as Administrator up-front is only a convenience to avoid repeated prompts during installers.

### Linux / macOS

- Use the `RUN_ME.sh` wrapper from the repository root. It changes into `files/` and runs `tools.sh`, which presents the interactive tools and installers:

```bash
./RUN_ME.sh
```

- If `RUN_ME.sh` is not executable, make it executable first:

```bash
chmod +x RUN_ME.sh
```

- Some install actions will prompt for elevated privileges (sudo) during execution. The program will request `sudo` when required; you do not need to run the whole helper with `sudo`.

```bash
sudo ./RUN_ME.sh  # optional: runs the wrapper with root privileges to avoid mid-run prompts
```

Running with `sudo` up-front is a convenience for unattended installs; otherwise run without `sudo` to inspect the menu and grant elevation only when prompted.

## Contributing

- Pull requests are welcome. If you add platform support or improve scripts, include clear instructions and testing notes.

## License

- This repository does not contain an explicit license file. If you plan to use or distribute the code, please confirm the licensing intent with the project owner.

## Support

- Open an issue or submit a PR with suggested edits or improvements.

Thanks for checking out ContOpsSync — pragmatic tooling for provisioning container tooling across systems.

## Small quirks noticed when coming back

- The default comment command is `--` meaning that `--help` will result in an unknown command
- The default command separator is `@#` however, for it to works it requires as space on either side.
- The default (if my memory is correct, intentional) behaviour of the terminal is to only exit when the `exit` command is called. However, this like the typical command prompt will only kill the current session one is in, there is another command called `abort` that is meant to exit any and all terminal sessions that are started, however, for some reason I haven't found a way to start a session within a session (other than using the run command which means that it is not internal), so for the moment, unless the underlying python program using the terminal creates sub runners (menus) this command doubles as the `exit` command.
- There is only one hardcoded argument flag `-nc` or `--no-colour`, this is case sensitive and is here to allow the user to disable colour displaying on the program, all the other arguments the user can pass are the programs actual commands that can be piped or typed into the interractive terminal itself.
- The colours themselves can be edited in the file `constants.py` and follow the windows Hexadecimal notaion logic (easier to chose from because less choice, so less overwhelming)
- There can be uncaught bugs in the program or it's modules, but they should not concern the system calls, they would mostly be due to parsing issues in python. If you find any please submit a bug.

# ContOpsSync

[![Static Badge](https://img.shields.io/badge/Buy_me_a_tea-Hanra-%235F7FFF?style=flat-square&logo=buymeacoffee&label=Buy%20me%20a%20coffee&labelColor=%235F7FFF&color=%23FFDD00&link=https%3A%2F%2Fwww.buymeacoffee.com%2Fhanra)](https://www.buymeacoffee.com/hanra)

ContOpsSync is a small Python utility to automate installation of Docker, Docker Compose, and Kubernetes-related tools across platforms.

## Status

Not actively developed; receives periodic dependency updates to keep it runnable on modern Python versions.

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

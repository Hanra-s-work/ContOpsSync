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

## Notes

- Some installers and platform-specific scripts are incomplete.
- Installer scripts reference official product pages where possible; behavior depends on those external sources.
- The project uses the small helper module `tty_ov` to simplify cross-platform system calls.

## Quick start

- Create a virtual environment (recommended) and install requirements if desired. See `files/requirements.txt` for dependencies.
- Run the main script from the repository root:

```
python src/main.py
```

## Contributing

- Pull requests are welcome. If you add platform support or improve scripts, include clear instructions and testing notes.

## License

- This repository does not contain an explicit license file. If you plan to use or distribute the code, please confirm the licensing intent with the project owner.

## Support

- Open an issue or submit a PR with suggested edits or improvements.

Thanks for checking out ContOpsSync — pragmatic tooling for provisioning container tooling across systems.

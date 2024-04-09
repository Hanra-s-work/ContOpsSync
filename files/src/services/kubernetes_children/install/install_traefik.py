"""
File in charge of installing traefik on the cluster
"""

import requests
import display_tty
from tqdm import tqdm
from tty_ov import TTY

class InstallTraefik:

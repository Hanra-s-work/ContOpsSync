"""
File in charge of checking the available ressources on the system
"""

import psutil
import platform
from datetime import datetime


class CheckSystemPerformance:
    """ Check the system performance """

    def __init__(self, success: int, err: int, error: int) -> None:
        self.success = success
        self.err = err
        self.error = error

        # ---- System info variables ----
        self.system_total_disk_size = 0
        self.system_used_disk_size = 0
        self.system_percent_used_disk_size = 0
        self.system_free_disk_size = 0
        self.system_percent_free_disk_size = 0
        self.system_ram = 0
        self.system_cpu = 0
        self.system_cores = 0
        self.system_gpu = 0
        self.system_threads = 0
        self.system_load = 0
        self.system_uptime = 0

        # ---- Human readable System info variables ----
        self.human_system_total_disk_size = 0
        self.human_system_used_disk_size = 0
        self.human_system_percent_used_disk_size = 0
        self.human_system_free_disk_size = 0
        self.human_system_percent_free_disk_size = 0
        self.human_system_ram = 0
        self.human_system_cpu = 0
        self.human_system_cores = 0
        self.human_system_gpu = 0
        self.human_system_threads = 0
        self.human_system_load = 0
        self.human_system_uptime = 0

    def get_system_total_disk_size(self) -> int:
        """ Get the system disk size """
        self.system_total_disk_size = psutil.disk_usage("/").total
        return self.system_total_disk_size

    def get_system_used_disk_size(self) -> int:
        """ Get the system disk size """
        self.system_used_disk_size = psutil.disk_usage("/").used
        return self.system_used_disk_size

    def get_system_free_disk_size(self) -> int:
        """ Get the system disk size """
        self.system_free_disk_size = psutil.disk_usage("/").free
        return self.system_free_disk_size

    def get_system_percent_used_disk_size(self) -> int:
        """ Get the system disk size """
        self.system_percent_used_disk_size = psutil.disk_usage("/").percent
        return self.system_percent_used_disk_size

    def get_system_percent_free_disk_size(self) -> int:
        """ Get the system disk size """
        self.system_percent_free_disk_size = (
            100 - psutil.disk_usage("/").percent
        )
        return self.system_percent_free_disk_size

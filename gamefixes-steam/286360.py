"""Shadows on the Vatican - Act I: Greed
Launcher keeps it's process running in the background but nothing shows up
"""

import os
from .. import util


def main() -> None:
    util.replace_command('SotV_Launcher.exe', 'hd/SotV1.exe')
    os.chdir('hd')

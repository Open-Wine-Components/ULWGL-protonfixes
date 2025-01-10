"""Game fix for Age of Mythology: Extended Edition
Source: https://github.com/JamesHealdUK/protonfixes/blob/master/fixes/266840.sh
"""

from .. import util


def main() -> None:
    """Changes the proton argument from the launcher to the game"""
    # Replace launcher with game exe in proton arguments
    util.replace_command('Launcher.exe', 'aomx.exe')

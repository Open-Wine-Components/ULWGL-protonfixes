"""Game fix for Age of Empires: DE"""

from .. import util


def main() -> None:
    """Changes the proton argument from the launcher to the game"""
    # Replace launcher with game exe in proton arguments
    util.append_argument('-NoStartup')

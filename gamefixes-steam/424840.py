"""Game fix for Little Nightmares"""

from .. import util


def main() -> None:
    """Add launch parameter"""
    # The game crashes if running with more than one CPU thread,
    # adding "-onethread" will force the game to use only one CPU thread
    util.append_argument('-onethread')

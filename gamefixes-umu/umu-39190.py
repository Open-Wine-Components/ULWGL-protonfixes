"""Game fix for Dungeon Siege"""

from .. import util


def main() -> None:
    """Apply protontricks directplay for full multiplayer functionality"""
    util.protontricks('directplay')

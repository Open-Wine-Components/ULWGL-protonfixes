"""Game fix for Dungeon Siege II"""

from .. import util


def main() -> None:
    """Apply protontricks directplay for full multiplayer functionality"""
    # Even though the Steam version has disabled multiplayer functionality
    # many people will apply a fix to unlock Broken Worlds which will also
    # enable multiplayer again.
    util.protontricks('directplay')

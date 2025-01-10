"""Game fix for Stronghold HD
Fixes Multiplayer
"""

from .. import util


def main() -> None:
    """Installs directplay"""
    util.protontricks('directplay')

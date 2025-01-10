"""Game fix for Total Annihilation"""

from .. import util


def main() -> None:
    """Multiplayer requires directplay for full functionality"""
    util.protontricks('directplay')

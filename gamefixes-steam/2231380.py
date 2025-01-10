"""Tom Clancy's Ghost Recon Breakpoint"""

from .. import util


def main() -> None:
    """Game ships with outdated uPlay launcher, which will not install to be able to start the game"""
    util.protontricks('ubisoftconnect')

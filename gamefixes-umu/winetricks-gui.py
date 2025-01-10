"""Call Winetricks GUI"""

from .. import util


def main() -> None:
    """Requires seccomp"""
    util.protontricks('gui')

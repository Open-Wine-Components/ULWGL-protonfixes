"""Game fix for Dirt 3 Complete Edition"""

from protonfixes import util


def main() -> None:
    """installs openal as redistributable install script is borked."""

    util.protontricks('openal')

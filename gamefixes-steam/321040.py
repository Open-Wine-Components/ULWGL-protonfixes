"""Game fix for Dirt 3 Complete Edition"""

from .. import util


def main() -> None:
    """Installs openal as redistributable install script is borked."""
    util.protontricks('openal')

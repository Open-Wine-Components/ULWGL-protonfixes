"""Game fix for You Need a Budget 4"""

from .. import util


def main() -> None:
    """Installs corefonts"""
    # https://github.com/ValveSoftware/Proton/issues/7
    util.protontricks('corefonts')

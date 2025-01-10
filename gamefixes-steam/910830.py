"""Game fix for Rebel Galaxy Outlaw"""

from .. import util


def main() -> None:
    """Installs mfc42"""
    # https://github.com/ValveSoftware/Proton/issues/4216
    util.protontricks('mfc42')

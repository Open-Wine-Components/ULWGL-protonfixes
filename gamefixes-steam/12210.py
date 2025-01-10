"""Game fix for GTA IV"""

from .. import util


def main() -> None:
    """Installs wmp11"""
    # Fixes Independence FM user radio station
    util.protontricks('wmp11')

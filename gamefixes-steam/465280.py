"""Game fix for Yesterday Origins"""

from .. import util


def main() -> None:
    """Set to win7"""
    # Fixes black screen during cutscenes.
    util.protontricks('win7')

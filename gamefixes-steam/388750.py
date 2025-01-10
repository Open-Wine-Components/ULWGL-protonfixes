"""Game fix for Chronophantasma Extend"""

from .. import util


def main() -> None:
    """Uses installs devenum wmp9"""
    # https://github.com/ValveSoftware/Proton/issues/703#issuecomment-416075961
    util.protontricks('devenum')
    util.protontricks('wmp9')

"""Madden NFL 21 needs vcrun2019 for online mode to work"""

from .. import util


def main() -> None:
    # Replace launcher with game exe in proton arguments
    util.protontricks('vcrun2019')

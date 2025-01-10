"""Oddworld: Stranger's Wrath HD"""

from .. import util


def main() -> None:
    util.protontricks('mfc90')  # The game crashes on launch without mfc90

"""Game fix for Assassin's Creed 2"""

from .. import util


def main() -> None:
    """Game ships with outdated and not working uPlay launcher."""
    util.protontricks('ubisoftconnect')

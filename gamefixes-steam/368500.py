"""Game fix for Assassin's Creed: Syndicate"""

from .. import util


def main() -> None:
    """Game ships with outdated and not working uPlay launcher."""
    util.protontricks('ubisoftconnect')

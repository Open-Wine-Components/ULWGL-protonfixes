"""Game fix for KINGDOM HEARTS -HD 1.5+2.5 ReMIX-"""

from .. import util


def main() -> None:
    """Game needs SteamDeck=1 for cutscenes to work."""
    util.set_environment('SteamDeck', '1')

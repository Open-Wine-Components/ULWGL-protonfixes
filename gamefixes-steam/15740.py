"""Game fix for Oddworld: Munch's Oddysee"""

from .. import util


def main() -> None:
    """Klite to fix videos
    prev version of this used devenum, quartz, wmp9 but that caused laggy intros
    """
    util.protontricks('klite')

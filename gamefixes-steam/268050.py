"""Game fix for The Evil Within(268050)"""

from .. import util


def main() -> None:
    """Changes the proton argument from the launcher to the game"""
    util.protontricks('win7')

    util.set_environment('PULSE_LATENCY_MSEC', '60')

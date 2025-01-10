"""Game fix for Recettear: An Item Shop's Tale"""

from protonfixes import util


def main() -> None:
    """Install directsound libraries"""
    util.protontricks('dmime')
    util.protontricks('dmloader')
    util.protontricks('dmsynth')
    util.protontricks('dmusic')
    util.protontricks('dsound')
    util.protontricks('dswave')
    util.winedll_override('streamci', util.DllOverride.NATIVE)
    util.protontricks('sound=alsa')

    """ Fix for audio stutter/desync
    """
    util.set_environment('PULSE_LATENCY_MSEC', '60')

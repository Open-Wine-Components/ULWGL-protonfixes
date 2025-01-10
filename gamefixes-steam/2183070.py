"""Game fix for Tokyo Necro"""

from .. import util


def main() -> None:
    """Installs xact, disable ESYNC, disable FSYNC"""
    # Fixes crash after typing then entering or clicking `search` within the game's terminal menu
    util.protontricks('xact')
    # Fixes hanging after typing then entering or clicking `search` within the game's terminal menu
    util.disable_esync()
    util.disable_fsync()
    # Fixes audio not playing for in-game videos
    util.disable_protonmediaconverter()

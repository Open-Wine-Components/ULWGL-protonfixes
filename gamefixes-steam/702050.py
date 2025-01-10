"""Game fix for The Song of Saya"""

from .. import util


def main() -> None:
    """Disable esync and fsync"""
    # Fixes random crashing during gameplay
    util.disable_esync()
    util.disable_fsync()

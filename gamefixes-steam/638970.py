"""Game fix for Yakuza 0"""

from .. import util


def main() -> None:
    """Disable FSYNC"""
    # Disable fsync to fix saving issues
    util.disable_fsync()

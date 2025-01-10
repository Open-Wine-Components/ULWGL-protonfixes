"""Game fix for Yakuza Kiwami"""

from .. import util


def main() -> None:
    """Disable FSYNC"""
    # Disable fsync to fix saving issues and hang on exit
    util.disable_fsync()

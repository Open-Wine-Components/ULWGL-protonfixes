"""Game fix for Flight Simulator 2020"""

from .. import util


def main() -> None:
    """Needs fastlaunch option"""
    # Fixes the startup process.
    util.append_argument('-FastLaunch')

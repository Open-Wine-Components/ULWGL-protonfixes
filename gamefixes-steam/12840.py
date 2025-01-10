"""Game fix for Dirt 2"""

from .. import util


def main() -> None:
    """This game uses GFWL, which causes it to fail to launch. xliveless is needed to get this working."""
    util.protontricks('xliveless')

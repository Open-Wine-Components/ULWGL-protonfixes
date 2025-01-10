"""Game fix for Order of Battle: World War II
Still missing intro video codecs
"""

from .. import util


def main() -> None:
    """Install corefonts"""
    # https://github.com/ValveSoftware/Proton/issues/639
    util.protontricks('corefonts')

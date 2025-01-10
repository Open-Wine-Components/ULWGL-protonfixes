"""Game fix for Darkest Hour: A Hearts of Iron Game"""

from .. import util


def main() -> None:
    """Set virtual desktop"""
    # https://github.com/ValveSoftware/Proton/issues/3338
    util.protontricks('vd=1280x720')

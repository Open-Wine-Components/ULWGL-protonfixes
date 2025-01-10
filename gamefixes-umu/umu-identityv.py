"""Game fix for Identity V"""

from .. import util


def main() -> None:
    # Fixes black screen on first launch
    util.protontricks('d3dcompiler_47')

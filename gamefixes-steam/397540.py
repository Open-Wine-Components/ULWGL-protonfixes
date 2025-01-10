"""Game fix for Borderlands 3"""

from .. import util


def main() -> None:
    """Borderlands 3 vcrun2019 fix"""
    # Fixes the startup process.
    util.protontricks('vcrun2019')
    util.protontricks('d3dcompiler_47')

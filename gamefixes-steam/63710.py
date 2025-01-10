"""Game fix for BIT.TRIP RUNNER"""

from .. import util


def main() -> None:
    """From: https://www.protondb.com/app/63710"""
    util.protontricks('d3dcompiler_43')
    util.protontricks('d3dx9_43')
    util.winedll_override('openal32', 'b')

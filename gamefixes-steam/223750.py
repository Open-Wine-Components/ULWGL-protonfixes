"""Fixes for DCS World Steam Edition"""

from protonfixes import util


def main() -> None:
    # Based on https://www.digitalcombatsimulator.com/en/support/faq/SteamDeck/
    util.protontricks('d3dx11_43')
    util.protontricks('d3dcompiler_43')
    util.protontricks('d3dcompiler_47')
    util.winedll_override('wbemprox', util.DllOverride.NATIVE)  # doesn't seem to be strictly needed

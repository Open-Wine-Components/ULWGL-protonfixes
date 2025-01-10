"""Game fix for Assetto Corsa"""

from protonfixes import util


def main() -> None:
    """Fixes default launcher and ACM."""
    util.protontricks('dotnet452')
    # Fixes Content Manager (black windows)
    util.protontricks('d3dx11_43')
    util.protontricks('d3dcompiler_47')
    util.winedll_override('dwrite', util.DllOverride.NATIVE_BUILTIN)
    util.protontricks('win10')
    util.set_environment('PULSE_LATENCY_MSEC', '60')

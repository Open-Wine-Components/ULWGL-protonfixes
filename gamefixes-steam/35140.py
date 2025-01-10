"""Game fix Batman Arkham Asylum
(Currently no contollers)
"""

from .. import util


def main() -> None:
    """Needs windxp, dotnet35, phyzx, d3dx9"""
    # Probably not needed when proton will be merged with newer wine
    # TODO Controllers fixes
    util.protontricks('d3dcompiler_43')
    util.protontricks('d3dx9_43')
    util.protontricks('physx')

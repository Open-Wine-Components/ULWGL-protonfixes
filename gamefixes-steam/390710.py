"""Game fix for SUGURI 2"""

from .. import util


def main() -> None:
    """Installs d3dxof"""
    # https://github.com/ValveSoftware/Proton/issues/970#issuecomment-420421289
    util.protontricks('d3dxof')

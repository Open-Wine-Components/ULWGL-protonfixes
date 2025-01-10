"""Game fix for Bejeweled 3"""

from .. import util


def main() -> None:
    """Game needs d3dcompiler_43 for dx10 mode, but still does not work. disabling dx10 mode allows dx9 mode to work with dxvk"""
    util.set_environment('PROTON_NO_D3D10', '1')

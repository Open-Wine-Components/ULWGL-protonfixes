"""Game fix for L.A. Noire"""

from .. import util


def main() -> None:
    """Installs d3dx9_43, d3dcompiler_43, d3dx11_43, d3dcompiler_47
    forces dx11 (enables intro cinematics) without editing settings.ini
    """
    # https://github.com/ValveSoftware/Proton/issues/544#issuecomment-826150012
    util.protontricks('d3dx9_43')
    util.protontricks('d3dcompiler_43')
    util.protontricks('d3dx11_43')
    util.protontricks('d3dcompiler_47')
    util.append_argument('-dx11')

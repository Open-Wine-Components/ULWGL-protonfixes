"""Game fix for Conception PLUS: Maidens of the Twelve Stars"""

from .. import util


def main() -> None:
    """Installs d3dcompiler_47"""
    # https://github.com/ValveSoftware/Proton/issues/3493#issuecomment-1521636321
    util.protontricks('d3dcompiler_47')

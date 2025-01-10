"""Crysis Remastered"""

from .. import util


def main() -> None:
    # Replace launcher with game exe in proton arguments
    util.protontricks('vcrun2019')
    util.protontricks('d3dcompiler_43')

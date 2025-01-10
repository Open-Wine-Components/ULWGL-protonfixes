"""Game fix for Star Trek Online launcher"""

from .. import util


def main() -> None:
    """Ensure d3dcompiler_47 is installed so the launcher window content is visible"""
    util.protontricks('d3dcompiler_47')

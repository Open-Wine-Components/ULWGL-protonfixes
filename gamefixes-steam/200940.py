"""Game fix for Sonic CD"""

from .. import util


def main() -> None:
    """Installs d3dcompiler_43, d3dx9_43, mdx. Locks fps to 60."""
    util.protontricks('d3dcompiler_43')
    util.protontricks('d3dx9_43')
    util.protontricks('mdx')

"""Game fix Catherine Classic"""

from .. import util


def main() -> None:
    util.protontricks('directshow')
    util.protontricks('cinepak')
    util.protontricks('lavfilters')
    util.protontricks('d3dcompiler_43')
    util.protontricks('d3dcompiler_47')
    util.disable_protonmediaconverter()

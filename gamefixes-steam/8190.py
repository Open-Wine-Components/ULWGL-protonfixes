"""Just Cause 2"""

from .. import util


def main() -> None:
    """Requires seccomp"""
    util.protontricks('d3dcompiler_43')
    util.protontricks('d3dcompiler_47')
    util.protontricks('d3dx10')
    util.append_argument('-borderless')

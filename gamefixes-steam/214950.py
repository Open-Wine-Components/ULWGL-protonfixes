"""Game fix for Total War: Rome II"""

from .. import util


def main() -> None:
    """Installs d3dcompiler_42, directplay
    Disable esync and fsync
    """
    util.protontricks('d3dcompiler_42')
    util.protontricks('directplay')
    util.disable_esync()
    util.disable_fsync()

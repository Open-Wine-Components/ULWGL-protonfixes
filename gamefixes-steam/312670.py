"""Game fix for Strange Brigade"""

from .. import util


def main() -> None:
    """This bypasses Strange Brigade's Launcher, which renders all black."""
    # Fixes the startup process.
    util.replace_command('StrangeBrigade.exe', 'StrangeBrigade_Vulkan.exe')
    util.append_argument('-skipdrivercheck -noHDR')

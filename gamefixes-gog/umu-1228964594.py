"""Game fix for Soldier of Fortune II: Double Helix - Gold Edition"""

from .. import util


def main() -> None:
    # Fix display issues
    util.set_environment('MESA_EXTENSION_MAX_YEAR', '2003')
    util.set_environment('__GL_ExtensionStringVersion', '17700')

"""Game fix for CYGNI: All Guns Blazing"""

from .. import util


def main() -> None:
    # EGS only: This fixes the startup process.
    util.append_argument('-epicdeploymentid=78a046d4ac1b42d7aaba9fe80f88a5d8')

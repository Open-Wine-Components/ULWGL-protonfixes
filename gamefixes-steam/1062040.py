"""Dragon Star Varnir"""

from .. import util


def main() -> None:
    """Dragon Star Varnir fix"""
    # Fixes the startup process.
    util.winedll_override('xactengine3_7', 'n')

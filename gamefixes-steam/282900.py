"""Hyperdimension Neptunia Re;Birth1
Poor performance on some AMD hardware
"""

from .. import util


def main() -> None:
    util.set_environment('radeonsi_disable_sam', 'true')
    util.set_environment('AMD_DEBUG', 'nowc')

"""Game fix for Mafia II Definitive Edition"""

from .. import util


def main() -> None:
    """Enable NVIDIA PhysX support."""
    util.protontricks('physx')

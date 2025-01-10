"""Game fix for Batman Arkham Knight"""

from .. import util


def main() -> None:
    """NVIDIA PhysX support."""
    # Enables NVIDIA PhysX in Batman Arkham Knight.
    util.protontricks('physx')

"""Game fix for The Forest"""

from .. import util


def main() -> None:
    """If SMT/HT is enabled, The Forest runs with extremely choppy. Just bad.
    We can fix it by setting the topology to the physical cores / core count.
    TODO: This fix was not tested with more than 10 physical cores yet.
    """
    util.set_cpu_topology_nosmt()

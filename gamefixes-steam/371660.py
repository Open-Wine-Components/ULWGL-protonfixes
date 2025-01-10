"""Far Cry Primal"""

from .. import util


def main() -> None:
    """Chokes on more than 31 cores"""
    util.set_cpu_topology_limit(31)

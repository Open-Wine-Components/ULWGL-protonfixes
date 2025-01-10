"""FarCry 3"""

from .. import util


def main() -> None:
    """FarCry 3 chokes on more than 24 cores"""
    util.set_cpu_topology_limit(24)

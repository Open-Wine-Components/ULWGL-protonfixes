"""Game fix for Lost Planet 2 (2010)
This game requires two fixes to work:
1. A mocked xlive.dll for GFWL (multiplayer will not work, but the single player does)
2. No more than 12 CPU cores (on PCGamingWiki is described as 6, but on my personal test I was able to set until 12 of 16) [source: https://www.pcgamingwiki.com/wiki/Lost_Planet_2#Alternate_solution_for_high_core_CPUs]
"""

from .. import util


def main() -> None:
    util.protontricks('xliveless')

    # According to PCGW, no more than 6 physical cores work
    # Nevertheless, the game was tested with 12 threads
    # TODO: Test the game with SMT disabled / use set_cpu_topology_nosmt()
    util.set_cpu_topology_limit(12)

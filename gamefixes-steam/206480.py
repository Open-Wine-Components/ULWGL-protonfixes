"""Game fix Dungeons & Dragons Online"""

from protonfixes import util


def main() -> None:
    """Disable libglesv2"""
    # gpu acceleration on wined3d https://bugs.winehq.org/show_bug.cgi?id=44985
    # Make the store work.
    util.winedll_override('libglesv2', util.DllOverride.DISABLED)

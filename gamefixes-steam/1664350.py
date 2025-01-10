"""Ship Graveyard Simulator Prologue"""

from .. import util


def main() -> None:
    """Needs builtin vulkan-1"""
    util.winedll_override('vulkan-1', 'b')

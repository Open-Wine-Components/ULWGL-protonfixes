"""Game fix for Watch_Dogs 2"""

from .. import util


def main() -> None:
    """Disable Easy Anti-Cheat and online play"""
    # Replace launcher with game exe in proton arguments
    util.append_argument('-eac_launcher -nosplash')

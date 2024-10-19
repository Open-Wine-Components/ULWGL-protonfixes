"""Game fix for Gothic 3"""

from protonfixes import util


def main() -> None:
    """Modify ge3.ini"""
    game_opts = """
    [Engine.Setup]
    Timer.ThreadSafe=false
    FpS.Max=0
    """

    util.set_ini_options(game_opts, 'Ini/ge3.ini', 'cp1251')

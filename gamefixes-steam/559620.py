"""Game fix for Outlaws + A Handful of Missions"""

from .. import util


def main() -> None:
    # Override ddraw (cutscenes+menu perf) and WinMM (Music)
    util.winedll_override('ddraw', 'n,b')
    util.winedll_override('winmm', 'n,b')

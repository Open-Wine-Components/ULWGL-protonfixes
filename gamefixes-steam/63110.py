"""Alter Ego
Launcher crashes immediately without displaying any windows
"""

from .. import util


def main() -> None:
    util.replace_command('AlterEgo.exe', './RunDev.exe')
    util.append_argument('AlterEgo.ebr')
    util.set_environment('SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS', '0')

"""The Night of the Rabbit
https://github.com/ValveSoftware/Proton/issues/1412
No cutscene audio in Daedalic Games (Memoria, The Night of the Rabbit, A New Beginning - Final Cut) (105000 230820 243200) #1412
"""

from .. import util


def main() -> None:
    util.winedll_override('xaudio2_7', 'd')

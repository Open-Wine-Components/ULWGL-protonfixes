"""Game fix Stealth Inc 2: A Game of Clones"""

from .. import util
from ..logger import log


def main() -> None:
    """Dsound is needed for audio"""
    log('Installing dsound')
    util.protontricks('dsound')

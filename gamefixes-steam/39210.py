"""Game fix for FFXIV"""

import os
from .. import util


def main() -> None:
    """FFXIV add NOSTEAM option."""
    # Fixes the startup process.
    if 'NOSTEAM' in os.environ:
        util.replace_command('-issteam', '')

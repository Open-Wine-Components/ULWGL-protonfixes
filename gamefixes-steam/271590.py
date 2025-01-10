"""Game fix for GTAV"""

import os
from .. import util


def main() -> None:
    """Game fix for GTAV"""
    # Rockstar reads SteamAppId and tries to init Steam API
    # We want to avoid this when running from Epic for example
    game_id = os.environ.get('UMU_ID')
    if game_id and not game_id.isnumeric():
        util.del_environment('SteamAppId')

"""Game fix for Red Dead Redemption 2"""

from .. import util


def main() -> None:
    """Sometimes game will not launch if -fullscreen -vulkan is not specified"""
    util.append_argument('-fullscreen -vulkan')
    # Set SteamGameId so that non-steam versions can pick up steam-specific fixes in proton's wine code
    util.set_environment('SteamGameId', '1174180')

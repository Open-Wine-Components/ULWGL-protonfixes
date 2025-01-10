"""Game fix for Gothic 1 Classic
Game fix for Gothic II: Gold Classic
"""

from .. import util


def main() -> None:
    # Fix resolution, not necessary with 'GD3D11' - but doesn't hurt
    set_resolution()

    # Fix background music / Gothic 2 startup
    util.protontricks('directmusic')
    util.winedll_override('*dsound', 'b')  # Override registry entry

    # Fix crackling audio
    util.set_environment('PULSE_LATENCY_MSEC', '90')

    # Allow use of the popular workshop item 'GD3D11', which implements the DirectDraw API with Gothic-specific fixes
    # Gothic 1: https://steamcommunity.com/sharedfiles/filedetails/?id=2791606767
    # Gothic 2: https://steamcommunity.com/sharedfiles/filedetails/?id=2787015529
    #
    # This might also be necessary for the GOG release
    util.winedll_override('ddraw', 'n,b')

    # Fix extreme mouse stutter and allow additional use of 'GRawInput (mouse fix)' from workshop
    # Gothic 1: https://steamcommunity.com/sharedfiles/filedetails/?id=3054112346
    # Gothic 2: https://steamcommunity.com/sharedfiles/filedetails/?id=3054078559
    util.winedll_override('dinput', 'n,b')


def set_resolution() -> None:
    # Patch the config to match the system resolution
    screen_width, screen_height = util.get_resolution()

    zVidResFullscreenX = str(screen_width)
    zVidResFullscreenY = str(screen_height)

    game_opts = (
        """
    [GAME]
    scaleVideos=1
    [VIDEO]
    zVidResFullscreenX="""
        + zVidResFullscreenX
        + """
    zVidResFullscreenY="""
        + zVidResFullscreenY
        + """
    zVidResFullscreenBPP=32
    """
    )

    util.set_ini_options(game_opts, 'system/Gothic.ini', 'cp1251', 'game')

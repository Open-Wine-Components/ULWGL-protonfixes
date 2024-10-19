"""Game fix for Space Engineers"""

from protonfixes import util


def main() -> None:
    util.protontricks('xaudio29')

    base_attibutte = '<runtime>'
    game_opts = """
  	<gcServer enabled = "true" />
"""

    util.set_xml_options(base_attibutte, game_opts, 'SpaceEngineers.exe.config')

    util.append_argument('-skipintro')

"""Game fix for Tomb Raider I"""

from .. import util


def main() -> None:
    """Enable Glide emulation in dosbox config"""
    conf_dict = {'glide': {'glide': 'emu'}}
    util.create_dosbox_conf('glide_fix.conf', conf_dict)
    util.append_argument('-conf')
    util.append_argument('glide_fix.conf')

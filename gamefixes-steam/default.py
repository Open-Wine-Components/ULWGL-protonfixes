"""Default file for Steam game fixes
This file is always executed for games that are identified as Steam games,
even if no game fix is present. It is run before game fixes are applied.
"""

import sys
from .. import util


def main() -> None:
    """Global defaults"""

    # Steam commandline
    def use_steam_commands() -> None:
        """Parse aliases from Steam launch options"""
        pf_alias_list = list(filter(lambda item: item.startswith('-pf_'), sys.argv))

        for pf_alias in pf_alias_list:
            alias, sep, param = pf_alias.partition('=')
            if sep != '=':
                continue
            sys.argv.remove(pf_alias)

            if alias == '-pf_tricks':
                util.protontricks(param)
            elif alias == '-pf_dxvk_set':
                dxvk_opt, dxvk_sep, dxvk_val = param.partition('=')
                if dxvk_sep == '=':
                    util.set_dxvk_option(dxvk_opt, dxvk_val)
            elif alias == '-pf_replace_cmd':
                repl_opt, repl_sep, repl_val = param.partition('=')
                if repl_sep == '=':
                    util.replace_command(repl_opt, repl_val)

    use_steam_commands()

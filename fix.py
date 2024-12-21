"""Gets the game id and applies a fix if found"""

import os
import re
import sys
import csv
from functools import lru_cache
from importlib import import_module

try:
    from . import config
    from .checks import run_checks
    from .logger import log
except ImportError:
    import config
    from checks import run_checks
    from logger import log

try:
    import __main__ as protonmain
except ImportError:
    log.warn('Unable to hook into Proton main script environment')


@lru_cache
def get_game_id() -> str:
    """Trys to return the game id from environment variables"""
    if 'UMU_ID' in os.environ:
        return os.environ['UMU_ID']
    if 'SteamAppId' in os.environ:
        return os.environ['SteamAppId']
    if 'SteamGameId' in os.environ:
        return os.environ['SteamGameId']
    if 'STEAM_COMPAT_DATA_PATH' in os.environ:
        return re.findall(r'\d+', os.environ['STEAM_COMPAT_DATA_PATH'])[-1]

    log.crit('Game ID not found in environment variables')
    return None


@lru_cache
def get_game_name() -> str:
    """Trys to return the game name from environment variables"""
    pfx = os.environ.get('WINEPREFIX') or protonmain.g_session.env.get('WINEPREFIX')
    script_dir = os.path.dirname(os.path.abspath(__file__))  # noqa: PTH100, PTH120

    if os.environ.get('UMU_ID'):
        if os.path.isfile(f'{pfx}/game_title'):  # noqa: PTH113
            with open(f'{pfx}/game_title', encoding='utf-8') as file:  # noqa: PTH123
                return file.readline()

        umu_id = os.environ['UMU_ID']
        store = os.getenv('STORE', 'none')
        csv_file_path = os.path.join(script_dir, 'umu-database.csv')  # noqa: PTH118

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:  # noqa: PTH123
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    # Check if the row has enough columns and matches both UMU_ID and STORE
                    if len(row) > 3 and row[3] == umu_id and row[1] == store:
                        title = row[0]  # Title is the first entry
                        with open(  # noqa: PTH123
                            os.path.join(script_dir, 'game_title'),  # noqa: PTH118
                            'w',
                            encoding='utf-8',
                        ) as file:
                            file.write(title)
                        return title
        except FileNotFoundError:
            log.warn(f'CSV file not found: {csv_file_path}')
        except Exception as ex:
            log.debug(f'Error reading CSV file: {ex}')

        log.warn('Game title not found in CSV')
        return 'UNKNOWN'

    try:
        log.debug('UMU_ID is not in environment')
        game_library = re.findall(r'.*/steamapps', os.environ['PWD'], re.IGNORECASE)[-1]
        game_manifest = os.path.join(game_library, f'appmanifest_{get_game_id()}.acf')  # noqa: PTH118

        with open(game_manifest, encoding='utf-8') as appmanifest:  # noqa: PTH123
            for xline in appmanifest.readlines():
                if 'name' in xline.strip():
                    name = re.findall(r'"[^"]+"', xline, re.UNICODE)[-1]
                    return name
    except (OSError, IndexError, UnicodeDecodeError):
        pass

    return 'UNKNOWN'


def get_store_name(store: str) -> str:
    """Mapping for store identifier to store name"""
    return {
        'amazon': 'Amazon',
        'battlenet': 'Battle.net',
        'ea': 'EA',
        'egs': 'EGS',
        'gog': 'GOG',
        'humble': 'Humble',
        'itchio': 'Itch.io',
        'steam': 'Steam',
        'ubisoft': 'Ubisoft',
        'zoomplatform': 'ZOOM Platform',
    }.get(store, None)


def get_module_name(game_id: str, default: bool = False, local: bool = False) -> str:
    """Creates the name of a gamefix module, which can be imported"""
    store = 'umu'
    if game_id.isnumeric():
        store = 'steam'
    elif os.environ.get('STORE'):
        store = os.environ.get('STORE').lower()

    if store != 'steam':
        log.info(f'Non-steam game {get_game_name()} ({game_id})')

        store_name = get_store_name(store)
        if store_name:
            log.info(f'{store_name} store specified, using {store_name} database')
        else:
            log.info('No store specified, using UMU database')
            store = 'umu'

    return (f'protonfixes.gamefixes-{store}.' if not local else 'localfixes.') + (
        game_id if not default else 'default'
    )


def _run_fix_local(game_id: str, default: bool = False) -> bool:
    """Check if a local gamefix is available first and run it"""
    localpath = os.path.expanduser('~/.config/protonfixes/localfixes')  # noqa: PTH111
    module_name = game_id if not default else 'default'

    # Check if local gamefix exists
    if not os.path.isfile(os.path.join(localpath, module_name + '.py')):  # noqa: PTH113, PTH118
        return False

    # Ensure local gamefixes are importable as modules via PATH
    with open(os.path.join(localpath, '__init__.py'), 'a', encoding='utf-8'):  # noqa: PTH118, PTH123
        sys.path.append(os.path.expanduser('~/.config/protonfixes'))  # noqa: PTH111

    # Run fix
    return _run_fix(game_id, default, True)


def _run_fix(game_id: str, default: bool = False, local: bool = False) -> bool:
    """Private function, which actually executes gamefixes"""
    fix_type = 'protonfix' if not default else 'defaults'
    scope = 'global' if not local else 'local'

    try:
        module_name = get_module_name(game_id, default, local)
        game_module = import_module(module_name)

        log.info(f'Using {scope} {fix_type} for {get_game_name()} ({game_id})')
        if hasattr(game_module, 'main_with_id'):
            game_module.main_with_id(game_id)
        else:
            game_module.main()
    except ImportError:
        log.info(f'No {scope} {fix_type} found for {get_game_name()} ({game_id})')
        return False
    return True


def run_fix(game_id: str) -> None:
    """Loads a gamefix module by it's gameid

    local fixes prevent global fixes from being executed
    """
    if game_id is None:
        return

    if config.enable_checks:
        run_checks()

    # execute default.py (local)
    if not _run_fix_local(game_id, True) and config.enable_global_fixes:
        _run_fix(game_id, True)  # global

    # execute <game_id>.py (local)
    if not _run_fix_local(game_id, False) and config.enable_global_fixes:
        _run_fix(game_id, False)  # global


def main() -> None:
    """Runs the gamefix"""
    check_args = [
        'iscriptevaluator.exe' in sys.argv[2],
        'getcompatpath' in sys.argv[1],
        'getnativepath' in sys.argv[1],
    ]

    if any(check_args):
        log.debug(str(sys.argv))
        log.debug('Not running protonfixes for setup runs')
        return

    log.info('Running protonfixes')
    run_fix(get_game_id())

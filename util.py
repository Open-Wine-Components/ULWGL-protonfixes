"""Utilities to make gamefixes easier"""

import configparser
import os
import sys
import re
import shutil
import signal
import tarfile
import zipfile
import subprocess
import urllib.request
import functools
from io import TextIOWrapper
from pathlib import Path
from socket import socket, AF_INET, SOCK_DGRAM
from typing import Literal, Any, Union, Optional
from collections.abc import Mapping, Generator, Callable

try:
    from .logger import log
    from .steamhelper import install_app
except ImportError:
    from logger import log
    from steamhelper import install_app

try:
    import __main__ as protonmain
except ImportError:
    log.warn('Unable to hook into Proton main script environment')

# TypeAliases
StrPath = Union[str, Path]
BasePathType = Literal['user', 'game']
OverrideTypes = Literal['n', 'b', 'n,b', 'b,n', '']


def protondir() -> str:
    """Returns the path to proton"""
    proton_dir = os.path.dirname(sys.argv[0])
    return proton_dir


def protonprefix() -> str:
    """Returns the wineprefix used by proton"""
    return os.path.join(os.environ['STEAM_COMPAT_DATA_PATH'], 'pfx/')


def protonnameversion() -> Optional[str]:
    """Returns the version of proton from sys.argv[0]"""
    version = re.search('Proton ([0-9]*\\.[0-9]*)', sys.argv[0])
    if version:
        return version.group(1)
    log.warn('Proton version not parsed from command line')
    return None


def protontimeversion() -> int:
    """Returns the version timestamp of proton from the `version` file"""
    fullpath = os.path.join(protondir(), 'version')
    try:
        with open(fullpath, encoding='ascii') as version:
            for timestamp in version.readlines():
                return int(timestamp.strip())
    except OSError:
        log.warn('Proton version file not found in: ' + fullpath)
        return 0
    log.warn('Proton version not parsed from file: ' + fullpath)
    return 0


def protonversion(timestamp: bool = False) -> Optional[Union[str, int]]:
    """Returns the version of proton"""
    if timestamp:
        return protontimeversion()
    return protonnameversion()


def once(
    func: Optional[Callable] = None, retry: bool = False
) -> Callable[..., Any]:
    """Decorator to use on functions which should only run once in a prefix.

    Error handling:
    By default, when an exception occurs in the decorated function, the
    function is not run again. To change that behavior, set retry to True.
    In that case, when an exception occurs during the decorated function,
    the function will be run again the next time the game is started, until
    the function is run successfully.
    Implementation:
    Uses a file (one per function) in PROTONPREFIX/drive_c/protonfixes/run/
    to track if a function has already been run in this prefix.
    """
    if func is None:
        return functools.partial(once, retry=retry)

    def wrapper(*args, **kwargs) -> None:  # noqa: ANN002, ANN003
        func_id = f'{func.__module__}.{func.__name__}'
        prefix = protonprefix()
        directory = os.path.join(prefix, 'drive_c/protonfixes/run/')
        file = os.path.join(directory, func_id)
        if not os.path.exists(directory):
            os.makedirs(directory)
        if os.path.exists(file):
            return

        exception = None
        try:
            func(*args, **kwargs)
        except Exception as exc:
            if retry:
                raise exc
            exception = exc

        with open(file, 'a', encoding='ascii') as tmp:
            tmp.close()

        if exception:
            raise exception

        return

    return wrapper


def _killhanging() -> None:
    """Kills processes that hang when installing winetricks"""
    # avoiding an external library as proc should be available on linux
    log.debug('Killing hanging wine processes')
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    badexes = ['mscorsvw.exe']
    for pid in pids:
        try:
            with open(os.path.join('/proc', pid, 'cmdline'), 'rb') as proc_cmd:
                cmdline = proc_cmd.read()
                for exe in badexes:
                    if exe in cmdline.decode():
                        os.kill(int(pid), signal.SIGKILL)
        except OSError:
            continue


def _forceinstalled(verb: str) -> None:
    """Records verb into the winetricks.log.forced file"""
    forced_log = os.path.join(protonprefix(), 'winetricks.log.forced')
    with open(forced_log, 'a', encoding='ascii') as forcedlog:
        forcedlog.write(verb + '\n')


def _checkinstalled(verb: str, logfile: str = 'winetricks.log') -> bool:
    """Returns True if the winetricks verb is found in the winetricks log"""
    if not isinstance(verb, str):
        return False

    winetricks_log = os.path.join(protonprefix(), logfile)

    # Check for 'verb=param' verb types
    if len(verb.split('=')) > 1:
        wt_verb = verb.split('=')[0] + '='
        wt_verb_param = verb.split('=')[1]
        wt_is_set = False
        try:
            with open(winetricks_log, encoding='ascii') as tricklog:
                for xline in tricklog.readlines():
                    if re.findall(r'^' + wt_verb, xline.strip()):
                        wt_is_set = bool(xline.strip() == wt_verb + wt_verb_param)
            return wt_is_set
        except OSError:
            return False
    # Check for regular verbs
    try:
        with open(winetricks_log, encoding='ascii') as tricklog:
            if verb in reversed([x.strip() for x in tricklog.readlines()]):
                return True
    except OSError:
        return False
    return False


def checkinstalled(verb: str) -> bool:
    """Returns True if the winetricks verb is found in the winetricks log or in the 'winetricks.log.forced' file"""
    if verb == 'gui':
        return False

    log.info(f'Checking if winetricks {verb} is installed')
    if _checkinstalled(verb, 'winetricks.log.forced'):
        return True
    return _checkinstalled(verb)


def is_custom_verb(verb: str) -> Union[bool, str]:
    """Returns path to custom winetricks verb, if found"""
    if verb == 'gui':
        return False

    verb_name = verb + '.verb'
    verb_dir = 'verbs'

    # check local custom verbs
    verbpath = os.path.expanduser('~/.config/protonfixes/localfixes/' + verb_dir)
    if os.path.isfile(os.path.join(verbpath, verb_name)):
        log.debug('Using local custom winetricks verb from: ' + verbpath)
        return os.path.join(verbpath, verb_name)

    # check custom verbs
    verbpath = os.path.join(os.path.dirname(__file__), verb_dir)
    if os.path.isfile(os.path.join(verbpath, verb_name)):
        log.debug('Using custom winetricks verb from: ' + verbpath)
        return os.path.join(verbpath, verb_name)

    return False


def check_internet() -> bool:
    """Checks for internet connection."""
    try:
        with socket(AF_INET, SOCK_DGRAM) as sock:
            sock.settimeout(5)
            sock.connect(('1.1.1.1', 53))
        return True
    except (TimeoutError, OSError):
        return False


def protontricks(verb: str) -> bool:
    """Runs winetricks if available"""
    if not checkinstalled(verb):
        if check_internet():
            # Proceed with your function logic here
            pass
        else:
            log.info('No internet connection. Winetricks will be skipped.')
            return False

        log.info('Installing winetricks ' + verb)
        env = dict(protonmain.g_session.env)
        env['WINEPREFIX'] = protonprefix()
        env['WINE'] = protonmain.g_proton.wine_bin
        env['WINELOADER'] = protonmain.g_proton.wine_bin
        env['WINESERVER'] = protonmain.g_proton.wineserver_bin
        env['WINETRICKS_LATEST_VERSION_CHECK'] = 'disabled'
        env['LD_PRELOAD'] = ''

        winetricks_bin = os.path.abspath(__file__).replace('util.py', 'winetricks')
        winetricks_cmd = [winetricks_bin, '--unattended'] + verb.split(' ')
        if verb == 'gui':
            winetricks_cmd = [winetricks_bin, '--unattended']

        # check is verb a custom winetricks verb
        custom_verb = is_custom_verb(verb)
        if custom_verb:
            winetricks_cmd = [winetricks_bin, '--unattended', custom_verb]

        if winetricks_bin is None:
            log.warn('No winetricks was found in $PATH')

        if winetricks_bin is not None:
            log.debug('Using winetricks command: ' + str(winetricks_cmd))

            # make sure proton waits for winetricks to finish
            for idx, arg in enumerate(sys.argv):
                if 'waitforexitandrun' not in arg:
                    sys.argv[idx] = arg.replace('run', 'waitforexitandrun')
                    log.debug(str(sys.argv))

            log.info('Using winetricks verb ' + verb)
            subprocess.call([env['WINESERVER'], '-w'], env=env)
            with subprocess.Popen(winetricks_cmd, env=env) as process:
                process.wait()
            _killhanging()

            # Check if the verb failed (eg. access denied)
            retc = process.returncode
            if retc != 0:
                log.warn(f'Winetricks failed running verb "{verb}" with status {retc}.')
                return False

            # Check if verb recorded to winetricks log
            if not checkinstalled(verb):
                log.warn(f'Not recorded as installed: winetricks {verb}, forcing!')
                _forceinstalled(verb)

            log.info('Winetricks complete')
            return True

    return False


def regedit_add(
    folder: str,
    name: Optional[str] = None,
    typ: Optional[str] = None,
    value: Optional[str] = None,
    arch: bool = False,
) -> None:
    """Add regedit keys"""
    env = dict(protonmain.g_session.env)
    env['WINEPREFIX'] = protonprefix()
    env['WINE'] = protonmain.g_proton.wine_bin
    env['WINELOADER'] = protonmain.g_proton.wine_bin
    env['WINESERVER'] = protonmain.g_proton.wineserver_bin

    if name is not None and typ is not None and value is not None:
        # Flag for if we want to force writing to the 64-bit registry sector
        if arch:
            regedit_cmd = [
                'wine',
                'reg',
                'add',
                folder,
                '/f',
                '/v',
                name,
                '/t',
                typ,
                '/d',
                value,
                '/reg:64',
            ]
        else:
            regedit_cmd = [
                'wine',
                'reg',
                'add',
                folder,
                '/f',
                '/v',
                name,
                '/t',
                typ,
                '/d',
                value,
            ]

        log.info('Adding key: ' + folder)

    else:
        # Flag for if we want to force writing to the 64-bit registry sector
        # We use name here because without the other flags we can't use the arch flag
        if name is not None:
            regedit_cmd = ['wine', 'reg', 'add', folder, '/f', '/reg:64']
        else:
            regedit_cmd = ['wine', 'reg', 'add', folder, '/f']

        log.info('Adding key: ' + folder)

    with subprocess.Popen(regedit_cmd, env=env) as process:
        process.wait()


def replace_command(
    orig: str, repl: str, match_flags: re.RegexFlag = re.IGNORECASE
) -> bool:
    """Make a commandline replacement in sys.argv

    Returns if there was any match.

    By default the search is case insensitive,
    you can override this behaviour with re.RegexFlag.NOFLAG
    """
    found = False
    for idx, arg in enumerate(sys.argv):
        replaced = re.sub(orig, repl, arg, flags=match_flags)
        if replaced == arg:
            continue
        sys.argv[idx] = replaced
        found = True

    if found:
        log.info(f'Changed "{orig}" to "{repl}"')
    else:
        log.warn(f'Can not change "{orig}" to "{repl}", command not found')
    return found


def append_argument(argument: str) -> None:
    """Append an argument to sys.argv"""
    log.info('Adding argument ' + argument)
    sys.argv.append(argument)
    log.debug('New commandline: ' + str(sys.argv))


def set_environment(envvar: str, value: str) -> None:
    """Add or override an environment value"""
    log.info(f'Adding env: {envvar}={value}')
    os.environ[envvar] = value
    protonmain.g_session.env[envvar] = value


def del_environment(envvar: str) -> None:
    """Remove an environment variable"""
    log.info('Removing env: ' + envvar)
    if envvar in os.environ:
        del os.environ[envvar]
    if envvar in protonmain.g_session.env:
        del protonmain.g_session.env[envvar]


def get_game_install_path() -> str:
    """Game installation path"""
    install_path = os.environ.get('STEAM_COMPAT_INSTALL_PATH', os.getcwd())
    log.debug(f'Detected path to game: {install_path}')
    return install_path


def winedll_override(dll: str, dtype: OverrideTypes) -> None:
    """Add WINE dll override"""
    log.info(f'Overriding {dll}.dll = {dtype}')
    setting = f'{dll}={dtype}'
    protonmain.append_to_env_str(
        protonmain.g_session.env, 'WINEDLLOVERRIDES', setting, ';'
    )


def patch_libcuda() -> bool:
    """Patches libcuda to work around games that crash when initializing libcuda and are using DLSS.

    We will replace specific bytes in the original libcuda.so binary to increase the allowed memory allocation area.

    The patched library is overwritten at every launch and is placed in .cache

    Returns true if the library was patched correctly. Otherwise returns false
    """
    cache_dir = os.path.expanduser('~/.cache/protonfixes')
    os.makedirs(cache_dir, exist_ok=True)

    try:
        # Use shutil.which to find ldconfig binary
        ldconfig_path = shutil.which('ldconfig')
        if not ldconfig_path:
            log.warn('ldconfig not found in PATH.')
            return False

        # Use subprocess.run with capture_output and explicit encoding handling
        try:
            result = subprocess.run(
                [ldconfig_path, '-p'], capture_output=True, check=True
            )
            # Decode the output using utf-8 with fallback to locale preferred encoding
            try:
                output = result.stdout.decode('utf-8')
            except UnicodeDecodeError:
                import locale

                encoding = locale.getpreferredencoding(False)
                output = result.stdout.decode(encoding, errors='replace')
        except subprocess.CalledProcessError as e:
            log.warn(f'Error running ldconfig: {e}')
            return False

        libcuda_path = None
        for line in output.splitlines():
            if 'libcuda.so' in line and 'x86-64' in line:
                # Parse the line to extract the path
                parts = line.strip().split(' => ')
                if len(parts) == 2:
                    path = parts[1].strip()
                    if os.path.exists(path):
                        libcuda_path = os.path.abspath(path)
                        break

        if not libcuda_path:
            log.warn('libcuda.so not found as a 64-bit library in ldconfig output.')
            return False

        log.info(f'Found 64-bit libcuda.so at: {libcuda_path}')

        patched_library = os.path.join(cache_dir, 'libcuda.patched.so')
        try:
            with open(libcuda_path, 'rb') as f:
                binary_data = f.read()
        except OSError as e:
            log.crit(f'Unable to read libcuda.so: {e}')
            return False

        # Replace specific bytes in the original libcuda.so binary to increase the allowed memory allocation area.
        # Context (see original comment here: https://github.com/jp7677/dxvk-nvapi/issues/174#issuecomment-2227462795):
        # There is an issue with memory allocation in libcuda.so when creating a Vulkan device with the
        # VK_NVX_binary_import and/or VK_NVX_image_view_handle extensions. libcuda tries to allocate memory in a
        # specific area that is already used by the game, leading to allocation failures.
        # DXVK and VKD3D work around this by recreating the device without these extensions, but doing so disables
        # DLSS (Deep Learning Super Sampling) functionality.
        # By modifying libcuda.so to increase the allowed memory allocation area, we can prevent these allocation
        # failures without disabling the extensions, thus enabling DLSS to work properly.
        # The hex replacement changes the memory allocation constraints within libcuda.so.

        hex_data = binary_data.hex()
        hex_data = hex_data.replace('000000f8ff000000', '000000f8ffff0000')
        patched_binary_data = bytes.fromhex(hex_data)

        try:
            with open(patched_library, 'wb') as f:
                f.write(patched_binary_data)

            # Set permissions to rwxr-xr-x (755)
            os.chmod(patched_library, 0o755)
            log.debug(f'Permissions set to rwxr-xr-x for {patched_library}')
        except OSError as e:
            log.crit(f'Unable to write patched libcuda.so to {patched_library}: {e}')
            return False

        log.info(f'Patched libcuda.so saved to: {patched_library}')
        set_environment('LD_PRELOAD', patched_library)
        return True

    except Exception as e:
        log.crit(f'Unexpected error occurred: {e}')
        return False


def disable_nvapi() -> None:
    """Disable WINE nv* dlls"""
    log.info('Disabling NvAPI')
    winedll_override('nvapi', '')
    winedll_override('nvapi64', '')
    winedll_override('nvcuda', '')
    winedll_override('nvcuvid', '')
    winedll_override('nvencodeapi', '')
    winedll_override('nvencodeapi64', '')


def disable_esync() -> None:
    """Disabling Esync"""
    log.info('Disabling Esync')
    set_environment('WINEESYNC', '')


def disable_fsync() -> None:
    """Disabling FSync"""
    log.info('Disabling FSync')
    set_environment('WINEFSYNC', '')


def disable_protonmediaconverter() -> None:
    """Disabling Proton Media Converter"""
    log.info('Disabling Proton Media Converter')
    set_environment('PROTON_AUDIO_CONVERT', '0')
    set_environment('PROTON_AUDIO_CONVERT_BIN', '0')
    set_environment('PROTON_VIDEO_CONVERT', '0')
    set_environment('PROTON_DEMUX', '0')


@once
def disable_uplay_overlay() -> bool:
    """Disables the UPlay in-game overlay.

    Creates or appends the UPlay settings.yml file
    with the correct setting to disable the overlay.
    UPlay will overwrite settings.yml on launch, but keep
    this setting.
    """
    config_dir = os.path.join(
        protonprefix(),
        'drive_c/users/steamuser/Local Settings/Application Data/Ubisoft Game Launcher/',
    )
    config_file = os.path.join(config_dir, 'settings.yml')

    os.makedirs(config_dir, exist_ok=True)

    try:
        data = (
            'overlay:\n'
            '  enabled: false\n'
            '  forceunhookgame: false\n'
            '  fps_enabled: false\n'
            '  warning_enabled: false\n'
            'user:\n'
            '  closebehavior: CloseBehavior_Close'
        )
        with open(config_file, 'a+', encoding='ascii') as file:
            file.write(data)
        log.info('Disabled UPlay overlay')
        return True
    except OSError as err:
        log.warn('Could not disable UPlay overlay: ' + err.strerror)

    return False


def create_dosbox_conf(
    conf_file: StrPath, conf_dict: Mapping[str, Mapping[str, Any]]
) -> None:
    """Create DOSBox configuration file.

    DOSBox accepts multiple configuration files passed with -conf
    option;, each subsequent one overwrites settings defined in
    previous files.
    """
    if os.access(conf_file, os.F_OK):
        return
    conf = configparser.ConfigParser()
    conf.read_dict(conf_dict)
    with open(conf_file, 'w', encoding='ascii') as file:
        conf.write(file)


def _get_case_insensitive_name(path: str) -> str:
    """Find potentially differently-cased location

    e.g /path/to/game/system/gothic.ini -> /path/to/game/System/GOTHIC.INI
    """
    if os.path.exists(path):
        return path
    root = path
    # Find first existing directory in the tree
    while not os.path.exists(root):
        root = os.path.split(root)[0]

    if root[len(root) - 1] not in ['/', '\\']:
        root = root + os.sep
    # Separate missing path from existing root
    s_working_dir = path.replace(root, '').split(os.sep)
    paths_to_find = len(s_working_dir)
    # Keep track of paths we found so far
    paths_found = 0
    # Walk through missing paths
    for directory in s_working_dir:
        if not os.path.exists(root):
            break
        dir_list = os.listdir(root)
        found = False
        for existing_dir in dir_list:
            # Find matching filename on drive
            if existing_dir.lower() == directory.lower():
                root = os.path.join(root, existing_dir)
                paths_found += 1
                found = True
        # If path was not found append case that we were looking for
        if not found:
            root = os.path.join(root, directory)
            paths_found += 1

    # Append rest of the path if we were unable to find directory at any level
    if paths_to_find != paths_found:
        root = os.path.join(root, os.sep.join(s_working_dir[paths_found:]))
    return root


def _get_config_full_path(cfile: StrPath, base_path: BasePathType) -> Optional[str]:
    """Find game's config file"""
    # Start from 'user'/'game' directories or absolute path
    if base_path == 'user':
        cfg_path = os.path.join(
            protonprefix(), 'drive_c/users/steamuser/My Documents', cfile
        )
    else:
        if base_path == 'game':
            cfg_path = os.path.join(get_game_install_path(), cfile)
        else:
            cfg_path = cfile
    cfg_path = _get_case_insensitive_name(str(cfg_path))

    if os.path.exists(cfg_path) and os.access(cfg_path, os.F_OK):
        log.debug('Found config file: ' + cfg_path)
        return cfg_path

    log.warn('Config file not found: ' + cfg_path)
    return None


def create_backup_config(cfg_path: str) -> None:
    """Create backup config file"""
    # Backup
    if not os.path.exists(cfg_path + '.protonfixes.bak'):
        log.info('Creating backup for config file')
        shutil.copyfile(cfg_path, cfg_path + '.protonfixes.bak')


def set_ini_options(
    ini_opts: str, cfile: StrPath, encoding: str, base_path: BasePathType = 'user'
) -> bool:
    """Edit game's INI config file"""
    cfg_path = _get_config_full_path(cfile, base_path)
    if not cfg_path:
        return False

    create_backup_config(cfg_path)

    # set options
    conf = configparser.ConfigParser(
        empty_lines_in_values=True, allow_no_value=True, strict=False
    )
    # Preserve option name case (default converts to lower case)
    conf.optionxform = lambda optionstr: optionstr

    conf.read(cfg_path, encoding)

    log.info(f'Addinging INI options into {cfile}:\n{str(ini_opts)}')
    conf.read_string(ini_opts)

    with open(cfg_path, 'w', encoding=encoding) as configfile:
        conf.write(configfile)
    return True


def set_xml_options(
    base_attibutte: str, xml_line: str, cfile: StrPath, base_path: BasePathType = 'user'
) -> bool:
    """Edit game's XML config file"""
    xml_path = _get_config_full_path(cfile, base_path)
    if not xml_path:
        return False

    create_backup_config(xml_path)

    # set options

    base_size = os.path.getsize(xml_path)
    backup_size = os.path.getsize(xml_path + '.protonfixes.bak')

    if base_size != backup_size:
        return False

    with open(xml_path, encoding='utf-8') as file:
        contents = file.readlines()
        i = 0
        for line in contents:
            i += 1
            if base_attibutte in line:
                log.info(f'Adding XML options into {cfile}, line {i}:\n{xml_line}')
                contents.insert(i, xml_line + '\n')

    with open(xml_path, 'w', encoding='utf-8') as file:
        for eachitem in contents:
            file.write(eachitem)

    log.info('XML config patch applied')
    return True


def get_resolution() -> tuple[int, int]:
    """Returns screen res width, height using xrandr"""
    # Execute xrandr command and capture its output
    xrandr_bin = os.path.abspath(__file__).replace('util.py', 'xrandr')
    xrandr_output = subprocess.check_output([xrandr_bin, '--current']).decode('utf-8')

    # Find the line that starts with 'Screen   0:' and extract the resolution
    for line in xrandr_output.splitlines():
        if 'primary' in line:
            resolution = line.split()[3]
            width_height = resolution.split('x')
            offset_values = width_height[1].split('+')
            clean_resolution = width_height[0] + 'x' + offset_values[0]
            screenx, screeny = clean_resolution.split('x')
            return (int(screenx), int(screeny))

    # If no resolution is found, return default values or raise an exception
    return (0, 0)  # or raise Exception('Resolution not found')


def read_dxvk_conf(cfp: TextIOWrapper) -> Generator[str, None, None]:
    """Add fake [DEFAULT] section to dxvk.conf"""
    yield f'[{configparser.ConfigParser().default_section}]'
    yield from cfp


def set_dxvk_option(
    opt: str, val: str, cfile: StrPath = '/tmp/protonfixes_dxvk.conf'
) -> None:
    """Create custom DXVK config file

    See https://github.com/doitsujin/dxvk/wiki/Configuration for details
    """
    conf = configparser.ConfigParser()
    # Preserve option name case (default converts to lower case)
    conf.optionxform = lambda optionstr: optionstr
    section = conf.default_section
    dxvk_conf = os.path.join(os.environ['PWD'], 'dxvk.conf')

    conf.read(cfile)

    if (
        not conf.has_option(section, 'session')
        or conf.getint(section, 'session') != os.getpid()
    ):
        log.info('Creating new DXVK config')
        set_environment('DXVK_CONFIG_FILE', str(cfile))

        conf = configparser.ConfigParser()
        # Preserve option name case (default converts to lower case)
        conf.optionxform = lambda optionstr: optionstr
        conf.set(section, 'session', str(os.getpid()))

        if os.access(dxvk_conf, os.F_OK):
            with open(dxvk_conf, encoding='ascii') as dxvk:
                conf.read_file(read_dxvk_conf(dxvk))
        log.debug(f'{conf.items(section)}')

    # set option
    log.info('Addinging DXVK option: ' + str(opt) + ' = ' + str(val))
    conf.set(section, opt, str(val))

    with open(cfile, 'w', encoding='ascii') as configfile:
        conf.write(configfile)


def install_eac_runtime() -> None:
    """Install Proton Easyanticheat Runtime"""
    install_app('1826330')


def install_battleye_runtime() -> None:
    """Install Proton BattlEye Runtime"""
    install_app('1161040')


def install_all_from_tgz(url: str, path: StrPath = os.getcwd()) -> None:
    """Install all files from a downloaded tar.gz"""
    cache_dir = os.path.expanduser('~/.cache/protonfixes')
    os.makedirs(cache_dir, exist_ok=True)
    tgz_file_name = os.path.basename(url)
    tgz_file_path = os.path.join(cache_dir, tgz_file_name)

    if tgz_file_name not in os.listdir(cache_dir):
        log.info('Downloading ' + tgz_file_name)
        urllib.request.urlretrieve(url, tgz_file_path)

    with tarfile.open(tgz_file_path, 'r:gz') as tgz_obj:
        log.info(f'Extracting {tgz_file_name} to {path}')
        tgz_obj.extractall(path)


def install_from_zip(url: str, filename: str, path: StrPath = os.getcwd()) -> None:
    """Install a file from a downloaded zip"""
    if filename in os.listdir(path):
        log.info(f'File {filename} found in {path}')
        return

    cache_dir = os.path.expanduser('~/.cache/protonfixes')
    os.makedirs(cache_dir, exist_ok=True)
    zip_file_name = os.path.basename(url)
    zip_file_path = os.path.join(cache_dir, zip_file_name)

    if zip_file_name not in os.listdir(cache_dir):
        log.info(f'Downloading {filename} to {zip_file_path}')
        urllib.request.urlretrieve(url, zip_file_path)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_obj:
        log.info(f'Extracting {filename} to {path}')
        zip_obj.extract(filename, path=path)


def try_show_gui_error(text: str) -> None:
    """Trys to show a message box with an error

    1. Try importing tkinter and show messagebox
    2. Try executing process 'notify-send'
    3. Failed, output info to log
    """
    try:  # in case in-use Python doesn't have tkinter, which is likely
        from tkinter import messagebox

        messagebox.showerror('Proton Fixes', text)
    except ImportError:
        try:
            subprocess.run(['notify-send', 'protonfixes', text], check=True)
        except (subprocess.SubprocessError, subprocess.CalledProcessError):
            log.info('Failed to show error message with the following text: ' + text)


def is_smt_enabled() -> bool:
    """Returns whether SMT is enabled.

    If the check has failed, False is returned.
    """
    try:
        with open('/sys/devices/system/cpu/smt/active', encoding='ascii') as smt_file:
            return smt_file.read().strip() == '1'
    except PermissionError:
        log.warn('No permission to read SMT status')
    except OSError as ex:
        log.warn(f'SMT status not supported by the kernel (errno: {ex.errno})')
    return False


def get_cpu_count() -> int:
    """Returns the cpu core count, provided by the OS.

    If the request failed, 0 is returned.
    """
    cpu_cores = os.cpu_count()
    if not cpu_cores or cpu_cores <= 0:
        log.warn('Can not read count of logical cpu cores')
        return 0
    return cpu_cores


def set_cpu_topology(core_count: int, ignore_user_setting: bool = False) -> bool:
    """This sets the cpu topology to a fixed core count.

    By default, a user provided topology is prioritized.
    You can override this behavior by setting `ignore_user_setting`.
    """
    # Don't override the user's settings (except, if we override it)
    user_topo = os.getenv('WINE_CPU_TOPOLOGY')
    if user_topo and not ignore_user_setting:
        log.info(f'Using WINE_CPU_TOPOLOGY set by the user: {user_topo}')
        return False

    # Sanity check
    if not core_count or core_count <= 0:
        log.warn('Only positive core_counts can be used to set cpu topology')
        return False

    # Format (example, 4 cores): 4:0,1,2,3
    cpu_topology = f'{core_count}:{",".join(map(str, range(core_count)))}'
    set_environment('WINE_CPU_TOPOLOGY', cpu_topology)
    log.info(f'Using WINE_CPU_TOPOLOGY: {cpu_topology}')
    return True


def set_cpu_topology_nosmt(
    core_limit: int = 0, ignore_user_setting: bool = False, threads_per_core: int = 2
) -> bool:
    """This sets the cpu topology to the count of physical cores.

    If SMT is enabled, eg. a 4c8t cpu is limited to 4 logical cores.
    You can limit the core count to the `core_limit` argument.
    """
    # Check first, if SMT is enabled
    if is_smt_enabled() is False:
        log.info('SMT is not active, skipping fix')
        return False

    # Currently (2024) SMT allows 2 threads per core, this might change in the future
    cpu_cores = get_cpu_count() // threads_per_core  # Apply divider
    cpu_cores = max(cpu_cores, min(cpu_cores, core_limit))  # Apply limit
    return set_cpu_topology(cpu_cores, ignore_user_setting)


def set_cpu_topology_limit(core_limit: int, ignore_user_setting: bool = False) -> bool:
    """This sets the cpu topology to a limited number of logical cores.

    A limit that exceeds the available cores, will be ignored.
    """
    cpu_cores = get_cpu_count()
    if core_limit >= cpu_cores:
        log.info(
            f'The count of logical cores ({cpu_cores}) is lower than '
            f'or equal to the set limit ({core_limit}), skipping fix'
        )
        return False

    # Apply the limit
    return set_cpu_topology(core_limit, ignore_user_setting)


def set_game_drive(enabled: bool) -> None:
    """Enable or disable the game drive setting.

    This function modifies the `compat_config` to include or exclude
    the "gamedrive" option based on the `enabled` parameter.

    Args:
        enabled (bool):
            If True, add "gamedrive" to `compat_config`.
            If False, remove "gamedrive" from `compat_config`.

    """
    if enabled:
        protonmain.g_session.compat_config.add('gamedrive')
    else:
        protonmain.g_session.compat_config.discard('gamedrive')

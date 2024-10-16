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

from pathlib import Path
from datetime import datetime, timezone
from socket import socket, AF_INET, SOCK_DGRAM
from typing import Literal, Any, Union, Optional
from collections.abc import Mapping, Callable

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


class ProtonVersion:
    """Parses the proton version and build timestamp"""

    def __init__(self, version_string: str) -> None:
        """Initialize from a given version string"""
        # Example string '1722141596 GE-Proton9-10-18-g3763cd3a\n'
        parts = version_string.split()
        if len(parts) != 2 or not parts[0].isnumeric():
            log.crit(f'Version string "{version_string}" is invalid!')
            return
        self.build_date: datetime = datetime.fromtimestamp(int(parts[0]), tz=timezone.utc)
        self.version_name: str = parts[1]


@functools.lru_cache
def protondir() -> Path:
    """Returns the path to proton"""
    return Path(sys.argv[0]).parent


@functools.lru_cache
def protonprefix() -> Path:
    """Returns the wineprefix used by proton"""
    return Path(os.environ.get('STEAM_COMPAT_DATA_PATH', '')) / 'pfx'


@functools.lru_cache
def proton_version() -> ProtonVersion:
    """Returns the version of proton"""
    fullpath = protondir() / 'version'
    try:
        version_string = fullpath.read_text(encoding='ascii')
        return ProtonVersion(version_string)
    except OSError:
        log.warn(f'Proton version file not found in: {fullpath}')
        return ProtonVersion('0 Unknown')


@functools.lru_cache
def which(appname: str) -> Union[str, None]:
    """Returns the full path of an executable in $PATH"""
    for path in os.environ['PATH'].split(os.pathsep):
        fullpath = os.path.join(path, appname)
        if os.path.exists(fullpath) and os.access(fullpath, os.X_OK):
            return fullpath
    log.warn(str(appname) + 'not found in $PATH')
    return None


def once(
    func: Union[Callable, None] = None, retry: bool = False
) -> Union[None, Callable[..., Any]]:
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
        directory = protonprefix() / 'drive_c/protonfixes/run/'
        file = directory / func_id
        if not directory.is_dir():
            directory.mkdir(parents=True)
        if file.is_file():
            return

        exception = None
        try:
            func(*args, **kwargs)
        except Exception as exc:
            if retry:
                raise exc
            exception = exc

        file.touch()

        if exception:
            raise exception

        return

    return wrapper


def _killhanging() -> None:
    """Kills processes that hang when installing winetricks"""
    # avoiding an external library as proc should be available on linux
    log.debug('Killing hanging wine processes')

    black_list = ['mscorsvw.exe']
    for path in Path('/proc').iterdir():
        try:
            cmd = path / 'cmdline'
            if not cmd.is_file():
                continue

            cmdline = cmd.read_text(encoding='ascii')
            if any([i in cmdline for i in black_list]):
                log.debug(f'Killing process #{path.stem}')
                os.kill(int(path.stem), signal.SIGKILL)
        except OSError as ex:
            log.debug(f'Failed to read cmd lines: {ex}')
            continue


def _forceinstalled(verb: str) -> None:
    """Records verb into the winetricks.log.forced file"""
    forced_log = protonprefix() / 'winetricks.log.forced'
    with forced_log.open('a') as file:
        file.write(f'{verb}\n')


def _checkinstalled(verb: str, logfile: str = 'winetricks.log') -> bool:
    """Returns True if the winetricks verb is found in the winetricks log"""
    if not isinstance(verb, str):
        return False

    winetricks_log = protonprefix() / logfile
    try:
        lines = winetricks_log.read_text(encoding='ascii').splitlines()
        lines = [line.strip() for line in lines]
        return verb in lines
    except OSError:
        log.warn(f'Can not check installed verbs for "{verb}" in file "{winetricks_log}".')
        return False


def checkinstalled(verb: str) -> bool:
    """Returns True if the winetricks verb is found in the winetricks log or in the 'winetricks.log.forced' file"""
    if verb == 'gui':
        return False

    log.info(f'Checking if winetricks "{verb}" is installed')
    if _checkinstalled(verb, 'winetricks.log.forced'):
        return True
    return _checkinstalled(verb)


def is_custom_verb(verb: str) -> Union[bool, Path]:
    """Returns path to custom winetricks verb, if found"""
    if verb == 'gui':
        return False

    verb_name = verb + '.verb'
    verb_dir = 'verbs'

    # check local custom verbs
    verb_path = (Path.home() / '.config/protonfixes/localfixes/') / verb_dir
    verb_file = verb_path / verb_name
    if verb_file.is_file():
        log.debug(f'Using local custom winetricks verb from: {verb_path}')
        return verb_file

    # check custom verbs
    verb_path = Path(__file__).parent / verb_dir
    verb_file = verb_path / verb_name
    if verb_file.is_file():
        log.debug(f'Using custom winetricks verb from: {verb_path}')
        return verb_file

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
        env['WINEPREFIX'] = str(protonprefix())
        env['WINE'] = protonmain.g_proton.wine_bin
        env['WINELOADER'] = protonmain.g_proton.wine_bin
        env['WINESERVER'] = protonmain.g_proton.wineserver_bin
        env['WINETRICKS_LATEST_VERSION_CHECK'] = 'disabled'
        env['LD_PRELOAD'] = ''

        winetricks_bin = Path(__file__).with_name('winetricks')
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
            log.debug(f'Using winetricks command: {winetricks_cmd}')

            # make sure proton waits for winetricks to finish
            for idx, arg in enumerate(sys.argv):
                if 'waitforexitandrun' not in arg:
                    sys.argv[idx] = arg.replace('run', 'waitforexitandrun')
                    log.debug(str(sys.argv))

            log.info(f'Using winetricks verb "{verb}"')
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
    name: Union[str, None] = None,
    typ: Union[str, None] = None,
    value: Union[str, None] = None,
    arch: bool = False,
) -> None:
    """Add regedit keys"""
    env = dict(protonmain.g_session.env)
    env['WINEPREFIX'] = str(protonprefix())
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


def get_game_install_path() -> Path:
    """Game installation path"""
    path = os.environ.get('STEAM_COMPAT_INSTALL_PATH')
    install_path = Path(path) if path else Path.cwd()
    log.debug(f'Detected path to game: {install_path}')
    return install_path


def winedll_override(dll: str, dtype: Literal['n', 'b', 'n,b', 'b,n', '']) -> None:
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
                    path = Path(parts[1].strip())
                    if path.is_file():
                        libcuda_path = path
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
        set_environment('LD_PRELOAD', str(patched_library))
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
    config_dir = protonprefix() / 'drive_c/users/steamuser/Local Settings/Application Data/Ubisoft Game Launcher/'
    config_file = config_dir / 'settings.yml'

    config_dir.mkdir(parents=True, exist_ok=True)

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
        with config_file.open('a', encoding='ascii') as file:
            file.write(data)
        log.info('Disabled UPlay overlay')
        return True
    except OSError as err:
        log.warn(f'Could not disable UPlay overlay: {err.strerror}')

    return False


def create_dosbox_conf(
    conf_file: str, conf_dict: Mapping[str, Mapping[str, Any]]
) -> None:
    """Create DOSBox configuration file.

    DOSBox accepts multiple configuration files passed with -conf
    option;, each subsequent one overwrites settings defined in
    previous files.
    """
    conf_file = Path(conf_file)
    if conf_file.is_file():
        return
    conf = configparser.ConfigParser()
    conf.read_dict(conf_dict)
    with conf_file.open('w', encoding='ascii') as file:
        conf.write(file)


def _get_case_insensitive_name(path: Path) -> Path:
    """Find potentially differently-cased location

    e.g /path/to/game/system/gothic.ini -> /path/to/game/System/GOTHIC.INI
    """
    # FIXME: Function could be replaced by glob with arg `case_sensitve=False` in Python 3.12
    if path.exists():
        return path

    # Parents are from nearest to farthest, we need to reverse them
    # The parents do not include the Path object itself.. obviously
    paths = list(reversed(path.parents)) + [path]
    resolved = paths[0]

    for i, part in enumerate(path.parts):
        current = resolved / part
        if current.exists():
            resolved = current
            continue

        # Mapping casefold file name in folder to it's Path()
        files = {file.name.casefold(): file for file in current.parent.iterdir()}
        cf_part = part.casefold()
        if cf_part in files:
            resolved = files[cf_part]
        else:
            unresolved = list(path.parts[i:])
            log.warn(f'Can not resolve case sensitive path "{path}", stopped after "{resolved}"')
            log.info(f'Returning resolved path, with non resolvable parts {unresolved} attached')
            return resolved / str.join('/', unresolved)

    log.debug(f'Resolved case sensitive path "{path}" -> "{resolved}"')
    return resolved


def _get_config_full_path(cfile: str, base_path: str) -> Optional[Path]:
    """Find game's config file"""
    # Start from 'user'/'game' directories or absolute path
    if base_path == 'user':
        cfg_path = protonprefix() / 'drive_c/users/steamuser/My Documents' / cfile
    elif base_path == 'game':
        cfg_path = get_game_install_path() / cfile
    else:
        cfg_path = Path(cfile)
    cfg_path = _get_case_insensitive_name(cfg_path)

    if cfg_path.is_file():
        log.debug(f'Found config file: {cfg_path}')
        return cfg_path

    log.warn(f'Config file not found: {cfg_path}')
    return None


def create_backup_config(cfg_path: Path) -> bool:
    """Create backup config file"""
    backup_path = cfg_path.with_name(cfg_path.name + '.protonfixes.bak')
    if not backup_path.is_file():
        log.info(f'Creating backup for config file "{cfg_path}" -> "{backup_path}"')
        shutil.copyfile(cfg_path, backup_path)
        return True
    return False


def set_ini_options(
    ini_opts: str, cfile: str, encoding: str, base_path: str = 'user'
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
    conf.optionxform = str

    conf.read(cfg_path, encoding)

    log.info(f'Addinging INI options into "{cfile}":\n{ini_opts}')
    conf.read_string(ini_opts)

    with cfg_path.open('w', encoding=encoding) as configfile:
        conf.write(configfile)
    return True


def set_xml_options(
    base_attibutte: str, xml_line: str, cfile: str, base_path: str = 'user'
) -> bool:
    """Edit game's XML config file"""
    xml_path = _get_config_full_path(cfile, base_path)
    if not xml_path:
        return False

    # Check if backup already exists
    if not create_backup_config(xml_path):
        return False

    # set options
    i = 0
    contents = xml_path.read_text(encoding='utf-8').splitlines()
    for line in contents:
        i += 1
        if base_attibutte not in line:
            continue
        log.info(f'Adding XML options into "{cfile}", line {i}:\n{xml_line}')
        contents.insert(i, xml_line + '\n')

    data = str.join('\n', contents)
    xml_path.write_text(data, encoding='utf-8')
    log.info('XML config patch applied')
    return True


def get_resolution() -> tuple[int, int]:
    """Returns screen res width, height using xrandr"""
    # Execute xrandr command and capture its output
    xrandr_bin = Path(__file__).with_name('xrandr')
    xrandr_output = subprocess.check_output([xrandr_bin, '--current'], text=True)

    # Example line: "DP-1 connected primary 5120x1440+0+0 (normal left inverted right x axis y axis) 1193mm x 336mm"
    res_match = re.search(r'connected primary (?P<x>\d{3,5})x(?P<y>\d{3,5})', xrandr_output)
    if not res_match:
        log.warn('Can not extract resolution from xrandr')
        return (0, 0) # or raise Exception('Resolution not found')
    
    x = res_match.group('x')
    y = res_match.group('y')
    return (int(x), int(y))


def set_dxvk_option(
    opt: str, val: str, cfile: Path = Path('/tmp/protonfixes_dxvk.conf')
) -> None:
    """Create custom DXVK config file

    See https://github.com/doitsujin/dxvk/wiki/Configuration for details
    """
    conf = configparser.ConfigParser()
    # Preserve option name case (default converts to lower case)
    conf.optionxform = lambda optionstr: optionstr
    conf.read(cfile)

    # FIXME: Python 3.13 implements `allow_unnamed_section=True`
    section = conf.default_section
    if conf.has_option(section, 'session') and conf.getint(section, 'session') == os.getpid():
        return

    log.info('Creating new DXVK config')
    set_environment('DXVK_CONFIG_FILE', str(cfile))

    conf = configparser.ConfigParser()
    # Preserve option name case (default converts to lower case)
    conf.optionxform = lambda optionstr: optionstr
    conf.set(section, 'session', str(os.getpid()))

    # Add configuration from game's directory
    dxvk_conf = get_game_install_path() / 'dxvk.conf'
    if dxvk_conf.is_file():
        text = dxvk_conf.read_text(encoding='ascii')
        conf.read_string(f'[{section}]\n{text}')

    log.debug(f'DXVK config:\n{conf.items(section)}')

    # set option
    log.info(f'Addinging DXVK option: "{opt}" = "{val}"')
    conf.set(section, opt, str(val))

    with cfile.open('w', encoding='ascii') as configfile:
        conf.write(configfile)


def install_eac_runtime() -> None:
    """Install Proton Easyanticheat Runtime"""
    install_app('1826330')


def install_battleye_runtime() -> None:
    """Install Proton BattlEye Runtime"""
    install_app('1161040')


def install_all_from_tgz(url: str, path: Path = get_game_install_path()) -> None:
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


def install_from_zip(url: str, filename: str, path: Path = get_game_install_path()) -> None:
    """Install a file from a downloaded zip"""
    if (path / filename).is_file():
        log.info(f'File "{filename}" found in "{path}"')
        return

    cache_dir = os.path.expanduser('~/.cache/protonfixes')
    os.makedirs(cache_dir, exist_ok=True)
    zip_file_name = os.path.basename(url)
    zip_file_path = os.path.join(cache_dir, zip_file_name)

    if not zip_file_path.is_file():
        log.info(f'Downloading "{filename}" to "{zip_file_path}"')
        urllib.request.urlretrieve(url, zip_file_path)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_obj:
        log.info(f'Extracting "{filename}" to "{path}"')
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

    Parameters
    ----------
    enabled : bool
        If True, add "gamedrive" to `compat_config`.
        If False, remove "gamedrive" from `compat_config`.

    Returns
    -------
    None

    """
    if enabled:
        protonmain.g_session.compat_config.add('gamedrive')
    else:
        protonmain.g_session.compat_config.discard('gamedrive')

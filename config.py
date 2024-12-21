"""Load configuration settings for protonfixes"""

from configparser import ConfigParser
from pathlib import Path

try:
    from .logger import log
except ImportError:
    from logger import log


CONF_FILE = '~/.config/protonfixes/config.ini'
DEFAULT_CONF = """
[main]
enable_checks = true
enable_splash = false
enable_global_fixes = true


[path]
cache_dir = ~/.cache/protonfixes
"""

CONF = ConfigParser()
CONF.read_string(DEFAULT_CONF)

try:
    CONF.read(Path(CONF_FILE).expanduser())

except Exception:
    log.debug('Unable to read config file ' + CONF_FILE)


def opt_bool(opt: str) -> bool:
    """Convert bool ini strings to actual boolean values"""
    return opt.lower() in ['yes', 'y', 'true', '1']


locals().update({x: opt_bool(y) for x, y in CONF['main'].items() if 'enable' in x})

locals().update({x: Path(y).expanduser() for x, y in CONF['path'].items()})

try:
    [
        Path(d).expanduser().mkdir(parents=True, exist_ok=True)
        for n, d in CONF['path'].items()
    ]
except OSError:
    pass

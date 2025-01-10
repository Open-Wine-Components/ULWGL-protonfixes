"""Game fix for Gothic Playable Teaser"""

from pathlib import Path
from protonfixes import util
from protonfixes.logger import log


def main() -> None:
    """Performance fixes and cleanup of excessive logs"""
    modify_settings()
    clear_logs()


def modify_settings() -> None:
    # Assure that the settings folder exists
    path = Path('GothicRemake/Saved/Config/WindowsNoEditor/')
    if not path.is_dir():
        log.info(f'Creating settings folder "{path}".')
        path.mkdir(parents=True, exist_ok=True)

    # Assure, that the settings file exists
    # Necessary defaults will still be created by the game
    path = path / 'Engine.ini'
    if not path.is_file():
        log.info(f'Creating empty settings file "{path}".')
        path.touch(exist_ok=True)

    # Disable excessive (as in gigabytes) logging
    # Disable motion blur / depth of field / lens flare
    game_opts = """
    [Core.Log]
    Global=off
    LogInteractiveProcess=all off

    [SystemSettings]
    r.MotionBlur.Max=0
    r.MotionBlurQuality=0
    r.DefaultFeature.MotionBlur=0
    r.DepthOfFieldQuality=0
    r.LensFlareQuality=0
    """
    util.set_ini_options(game_opts, path)


def clear_logs() -> None:
    # Clear all logs > 10 MB
    log_files = Path('GothicRemake/Saved/Logs').glob('*.log')
    for file in log_files:
        file_size = file.stat().st_size  # Bytes
        file_size = file_size // 1000 // 1000  # Megabytes
        if file.is_file() and file_size > 10:
            log.info(f'Removing log file "{file}" with a size of {file_size} MB.')
            file.unlink()

"""Game fix for FFX/X-2 HD Remaster"""

from protonfixes import util


def main() -> None:
    # Game defaults to Japanese language, set this to English instead
    config_path = (
        util.protonprefix()
        / 'drive_c/users/steamuser/My Documents/'
          'SQUARE ENIX/FINAL FANTASY X&X-2 HD Remaster'
    )

    # Ensure path exists
    config_path.mkdir(parents=True, exist_ok=True)

    # Find / create config file
    config_file = config_path / 'GameSetting.ini'
    config_file.touch()

    # Apply patch
    config = config_file.read_text(encoding='utf-8')
    if 'Language' in config:
        return

    config += '\nLanguage=en'
    config_file.write_text(config, encoding='utf-8')

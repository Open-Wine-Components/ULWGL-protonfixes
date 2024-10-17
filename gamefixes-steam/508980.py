"""Game fix for Crashday Redline Edition"""

import json
from protonfixes import util


def main() -> None:
    """Change setting FSAA to 0 in graphics.config"""
    config = (
        util.protonprefix()
        / 'drive_c/users/steamuser/Local Settings/'
          'Application Data/Crashday/config/graphics.config'
    )

    # https://stackoverflow.com/a/45435707
    with config.open(encoding='utf-8') as file:
        json_data: dict = json.load(file)

    # Attempt to change FSAA parameter
    if json_data.get('FSAA') != 0:
        json_data['FSAA'] = 0
    else:
        return

    # Only write, if config was alternated
    with config.open('w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4)

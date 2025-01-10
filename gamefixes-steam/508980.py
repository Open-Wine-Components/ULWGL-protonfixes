"""Game fix for Crashday Redline Edition"""

import json
from .. import util


def main() -> None:
    """Change setting FSAA to 0 in graphics.config"""
    config = (
        util.protonprefix()
        + 'drive_c/users/steamuser/Local Settings/'
        + 'Application Data/Crashday/config/graphics.config'
    )

    # https://stackoverflow.com/a/45435707
    with open(config, encoding='utf-8') as file:
        json_data = json.load(file)
        if 'FSAA' in json_data:
            json_data['FSAA'] = 0
    with open(config, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4)

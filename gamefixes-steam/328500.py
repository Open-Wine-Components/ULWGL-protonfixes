"""Game fix for Potatoman Seeks the Troof"""

from protonfixes import util


def main() -> None:
    """The file mms.cfg must contain the string `OverrideGPUValidation=1`"""
    flash_path = util.get_path_syswow64() / 'Macromed/Flash'
    flash_path.mkdir(parents=True, exist_ok=True)

    mms_path = flash_path / 'mms.cfg'
    if not mms_path.is_file():
        return

    mms = mms_path.read_text(encoding='utf-8')
    if 'OverrideGPUValidation' in mms:
        return

    mms += '\nOverrideGPUValidation=1'
    mms_path.write_text(mms, encoding='utf-8')

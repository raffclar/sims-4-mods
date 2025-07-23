import os

from save_backup.mod_logging import logger


def get_local_game_version(game_folder: str):
    version_file = os.path.join(game_folder, "GameVersion.txt")

    try:
        with open(version_file, "r") as f:
            version = f.read().strip()
            version = ''.join(c for c in version if c.isalnum() or c == '.')
            logger.info(f"Detected game version: {version}")
            return version
    except Exception:
        logger.exception(f"Error reading game version")
        raise

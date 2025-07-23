import os
import shutil
import time
import traceback
import sims4.commands

from save_backup.mod_logging import logger
from save_backup.version_reader import get_local_game_version

# Create an instance of the mod when the script is loaded
_command_type = sims4.commands.CommandType.Live



def generic_command(command_name):
    """
    Decorator to create a generic command with the specified name
    """
    def command(function):
        @sims4.commands.Command(command_name, command_type=_command_type)
        def wrapper(*args, _connection=None):
            output = sims4.commands.CheatOutput(_connection)
            # noinspection PyBroadException
            try:
                function(*args, _connection)
            except Exception as ex:
                tb = traceback.format_exc()
                output(tb)
                logger.exception("Failed to execute command")

    return command


def _get_game_folder():
    """
    Returns the base game folder path by navigating from the mod's location
    """
    # Get the directory where this module is located
    mod_dir = os.path.dirname(os.path.abspath(__file__))

    # From the mod directory, navigate up to the game's base directory
    # Typical path: <game_folder>/Mods/save_backup/save_backup/<file_name>.py
    # We need to go up 3 levels to reach the game folder
    game_folder = os.path.abspath(os.path.join(mod_dir, "..", "..", ".."))
    return game_folder



class SaveBackupConfig:
    GAME_FOLDER = _get_game_folder()
    # Default backup location (can be changed in settings)
    BACKUP_FOLDER = os.path.join(_get_game_folder(), "saves_backup")
    # Maximum number of backups to keep per version
    MAX_BACKUPS = 3
    # Maximum number of version to back up between game updates
    MAX_BACKUPS_VERSIONS = 4


def setup_backup_folder():
    """Create the backup folder if it doesn't exist"""
    if not os.path.exists(SaveBackupConfig.BACKUP_FOLDER):
        os.makedirs(SaveBackupConfig.BACKUP_FOLDER)
        logger.info(f"Created backup folder at {SaveBackupConfig.BACKUP_FOLDER}")

def backup_saves():
    """Backup all current save files"""
    saves_folder = os.path.join(SaveBackupConfig.GAME_FOLDER, "Saves")
    if not os.path.exists(saves_folder):
        logger.error(f"Saves folder not found at {saves_folder}")
        return

    current_time = time.strftime("%B_%d_%Y_%H_%M")

    # Find all save folders
    save_files = [f for f in os.listdir(saves_folder) if not os.path.isdir(os.path.join(saves_folder, f))]
    # Remove scratch folder
    save_files = [f for f in save_files if f != "scratch"]
    version_specific_backup_folder = os.path.join(
        SaveBackupConfig.BACKUP_FOLDER,
        get_local_game_version(SaveBackupConfig.GAME_FOLDER).replace(".", "_")
    )
    backup_folder = os.path.join(
        version_specific_backup_folder,
        current_time
    )
    os.makedirs(backup_folder, exist_ok=True)

    for save in save_files:
        save_path = os.path.join(saves_folder, save)
        save_backup_path = os.path.join(backup_folder, save)
        shutil.copyfile(save_path, save_backup_path)
        logger.info(f"Created backup of {save} at {save_backup_path}")

    # Manage backup limit if configured.
    if SaveBackupConfig.MAX_BACKUPS > 0:
        _cleanup_old_backups(version_specific_backup_folder, SaveBackupConfig.MAX_BACKUPS)
    # Manage version specific backup folders
    if SaveBackupConfig.MAX_BACKUPS_VERSIONS > 0:
        _cleanup_old_backups(SaveBackupConfig.BACKUP_FOLDER, SaveBackupConfig.MAX_BACKUPS)


def _cleanup_old_backups(backup_folder, max_backups):
    """Remove old backups if exceeding the maximum number"""
    backups = [os.path.join(backup_folder, d) for d in os.listdir(backup_folder)
               if os.path.isdir(os.path.join(backup_folder, d))]

    # Sort by creation time (oldest first)
    backups.sort(key=lambda x: os.path.getctime(x))

    # Remove oldest backups if exceeding limit
    while len(backups) > max_backups:
        oldest = backups.pop(0)
        shutil.rmtree(oldest)
        logger.info(f"Removed old backup: {oldest}")


# Command to manually trigger backup
@generic_command("auto_backup_saves")
def create_backup(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output("Creating save backup")
    backup_saves()
    output("Save backup created")


# Immediately begin backup at game start
backup_saves()

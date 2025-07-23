# Sims 4 Auto Backup Save Mod

## Overview
The Sims 4 Auto Backup Save Mod automatically creates backups of your save files to protect against save corruption,
accidental deletions, or game updates. The mod creates backups at game startup and provides an in-game command to 
create manual backups whenever needed.

## Features
- **Automatic Backups**: Creates backups of all save files when you start the game
- **Manual Backups**: Trigger backups on demand with a simple cheat command
- **Version Control**: Organizes backups by game version to prevent issues when updating (up to 4 versions)
- **Space Management**: Automatically cleans up old backups to prevent excessive disk usage (up to 3 backups per game version)
- **Time Stamping**: Each backup is labeled with date and time in 24-hour format

## Installation
1. Download the mod file
2. Place the downloaded file in your Mods folder:
    ```
    Documents/Electronic Arts/The Sims 4/Mods
    ```
3. Ensure that mods and script mods are enabled in your game options

## Usage

### Automatic Backups
The mod will automatically create backups of all your save files when you start the game. No action required!

### Manual Backups
To manually create a backup at any time:
1. Open the cheat console by pressing `Ctrl+Shift+C`
2. Type `auto_backup_saves` and press Enter
3. You'll see a confirmation message when the backup completes

## Configuration

By default, the mod:
- Stores backups in `Documents/Electronic Arts/The Sims 4/saves_backup`
- Keeps up to 3 backups per game version
- Keeps up to 4 different game version backup folders

## Backup Structure
- Each backup is stored in a folder with the format: `[Game Version]/[Date_Time]`
- Example: `1_93_263/January_15_2023_14_30`
- Game versions use underscores instead of periods for folder compatibility

## Troubleshooting
If you encounter issues:
- Check that script mods are enabled in your game settings
- Verify you have sufficient disk space for backups. Sims 4 games saves can become very large
- Ensure you have write permissions for the backup directory

## Compatibility
- Should work with most other mods
- No known conflicts with other save management mods

## Support
For questions, bug reports, or feature requests, please message ParametricPolymorphism on https://modthesims.info.

import logging
from zipfile import PyZipFile, ZIP_STORED, ZipFile

import shutil

import io
import fnmatch
import os


_logger = logging.getLogger(__name__)



script_package_types = ['*.zip', '*.ts4script']

def compile_module(source_mod_folder, target_mod_folder):
    for a_mod in os.listdir(source_mod_folder):
        ts4script_mods = os.path.join(target_mod_folder, os.path.basename(a_mod) + '.ts4script')
        zf = PyZipFile(ts4script_mods, mode='w', compression=ZIP_STORED, allowZip64=True, optimize=2)
        _logger.info("Compiling %s" % a_mod)
        for folder, subs, files in os.walk(os.path.join(source_mod_folder, a_mod)):
            if os.path.basename(folder) == "__pycache__":
                continue
            _logger.info(f"Adding folder: {folder}")
            zf.writepy(folder)
        zf.close()
        # shutil.copyfile(ts4script, ts4script_mods)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    compile_module(
        '../My Script Mods',
        '../../',
    )

from distutils.core import setup
from py2exe.py2exe_util import add_icon
import sys, os, shutil, py2exe

outfile = "Console.exe"

if len(sys.argv) < 2:
    sys.argv.append('py2exe')
setup(
        name="MyAppWalker",
        console=['bin/app_walker.py'],
        script = "bin/app_walker.py",
        options = {"py2exe": {"compressed": 1,
                              "optimize": 2,
                              "packages": [],
                              "includes": [
                                    "encodings.utf_8",
                                    "encodings.cp437",
                                    "encodings.mbcs",
                                    "distutils.dir_util",                                
                               ],
                              "bundle_files": 1}},
        zipfile = 'lib/Console.dll',
        data_files=[],
        dest_base = "AppWalker",

)

exe_path = os.path.abspath(os.path.join("dist","app_walker.exe"))
new_path = os.path.abspath(os.path.join("dist",outfile))
shutil.move(exe_path, new_path)
icon = os.path.abspath("Build\ShellI.ico")
add_icon(unicode(new_path), unicode(icon), 1)

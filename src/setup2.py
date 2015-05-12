"""
The contents of this file are subject to the PyTis Public License Version
1.1 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at
http://www.PyTis.com/License/

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
for the specific language governing rights and limitations under the
License.
"""
# This setup program will compile the Console application to run in the command
# line on Windows as Console.exe.  On Linux, simply run "python
# bin/app_walker.py"

import os

from py2exe.py2exe_util import add_icon
import sys, shutil, py2exe
# Updates version number in config.ini

version = '1.2'
outfile = "Console.exe"


print "Setup for version: %s" % version

import sys
try:
    import py2exe.mf as modulefinder
    import win32com
    import win32file
    modulefinder.AddPackagePath("win32file", win32file.__file__)
    
    for p in win32com.__path__[1:]:
        modulefinder.AddPackagePath("win32com", p)
    
    for extra in ["win32com.shell","win32com.mapi"]:
        __import__(extra)
        m = sys.modules[extra]
        for p in m.__path__[1:]:
            modulefinder.AddPackagePath(extra, p)
except ImportError:
    # no build path setup, no worries.
    pass

from distutils.core import setup
import py2exe


def main():
    # If run without args, build executables, in quiet mode.
    if len(sys.argv) == 1:
        sys.argv.append("py2exe")
        sys.argv.append("-q")

    class Target:
        def __init__(self, **kw):
            self.__dict__.update(kw)
            self.version = "%s" % version
            self.company_name = "PyTis.com"
            self.copyright = "Copyright (c) 2004-2009"
            self.name = "PyTis.com - another tool by Josh Lee"



    ################################################################

    setup(
        options = {"py2exe": {"compressed": 1,
                              "optimize": 2,
                              "ascii": 1,
                              "packages": [
                                   'win32com.gen_py',
                                   'wx.lib'
                                   
                               ],
                              "includes": [
                                    "encodings.utf_8",
                                    "encodings.cp437",
                                    "encodings.mbcs",
                                    "distutils.dir_util",                                
                               ],
                              "bundle_files": 1
                              }},
        console=['bin/app_walker.py'],
        zipfile = 'lib/Console.dll',
        data_files=[]
        
        )

if __name__ == '__main__':

    build = open("dist/lib/logs/BUILD.txt", 'w')
    sys.stdout = build
    main()
    sys.stdout = sys.__stdout__
    build.close()
    
    
    exe_path = os.path.abspath(os.path.join("dist","app_walker.exe"))
    new_path = os.path.abspath(os.path.join("dist",outfile))
    shutil.move(exe_path, new_path)
    icon = os.path.abspath("Build\PyTisNSIS.ico")
    add_icon(unicode(new_path), unicode(icon), 1)
    print "DONE"

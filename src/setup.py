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
# This setup program will compile the GUI application to run on Windows.  To
# run uncompiled you will need python and wxPython installed, and may run
# "python Builder.py"

import os

from py2exe.py2exe_util import add_icon
import sys, shutil, py2exe
# Updates version number in config.ini

version = '1.2'
outfile = "WalkerGUI.exe"


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


    manifest_template = '''
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <assemblyIdentity
        version="5.0.0.0"
        processorArchitecture="x86"
        name="%(prog)s"
        type="win32"
    />
    <description>%(prog)s Program</description>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity
                type="win32"
                name="Microsoft.Windows.Common-Controls"
                version="6.0.0.0"
                processorArchitecture="X86"
                publicKeyToken="6595b64144ccf1df"
                language="*"
            />
        </dependentAssembly>
    </dependency>
    </assembly>
    '''

    RT_MANIFEST = 24

    app = Target(
        # used for the versioninfo resource
        description = "PyTis.com - another tool by Josh Lee",

        # what to build
        script = "Builder.py",
        other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="pytis"))],
        icon_resources = [(1, "../images/WindowI.ico")],
        dest_base = "Builder")

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
   #     console=['bin/app_walker.py'],
        windows = [app],
        zipfile = 'lib/NSISWalker.dll',
        data_files=[("lib/settings",
                     ["lib/settings/config.ini"]),
                    
                    ("lib/settings/language",
                     ["lib/settings/language/lang.de",
                    "lib/settings/language/lang.en",
                    "lib/settings/language/lang.es",
                    "lib/settings/language/lang.fr",
                    "lib/settings/language/lang.it"]),
                
                 ]
        
        )

if __name__ == '__main__':
    path = os.path.dirname(__file__)
    for d in  [os.path.abspath(os.path.join(path, 'dist')),
               os.path.abspath(os.path.join(path, 'dist', 'lib')),
                 os.path.abspath(os.path.join(path, 'dist', 'lib', 'logs')),
                 os.path.abspath(os.path.join(path, 'dist', 'lib', 'settings')),
                 os.path.abspath(os.path.join(path, 'dist', 'lib', 'settings', 'language'))]:
        if not os.path.isdir(d):
            os.mkdir(d)
    
    shutil.copy('lib/settings/language/lang.de', 'dist/lib/settings/language/lang.de')
    shutil.copy('lib/settings/language/lang.en', 'dist/lib/settings/language/lang.en')
    shutil.copy('lib/settings/language/lang.es', 'dist/lib/settings/language/lang.es')
    shutil.copy('lib/settings/language/lang.fr', 'dist/lib/settings/language/lang.fr')
    shutil.copy('lib/settings/language/lang.it', 'dist/lib/settings/language/lang.it')
    
    
    build = open("dist/lib/logs/BUILD.txt", 'w')
    sys.stdout = build
    main()
    sys.stdout = sys.__stdout__
    build.close()
    
    
    exe_path = os.path.abspath(os.path.join("dist","Builder.exe"))
    new_path = os.path.abspath(os.path.join("dist",outfile))
    shutil.move(exe_path, new_path)
    icon = os.path.abspath("..\images\WindowI.ico")
    add_icon(unicode(new_path), unicode(icon), 1)
    print "DONE"

###############################################################################
# The contents of this file are subject to the PyTis Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.PyTis.com/License/
# 
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
###############################################################################
# ENGLISH LANGUAGE TRANSLATION FILE
#
# VALUES with Commas in them must be surrounded by " "'s
# VALUES with Percent '%' in them must be surrounded by " "'s
#
# Multi line values start with 3 quotes, """ or """ and end with the same 
# three quotes
###############################################################################
# Program Specific

title = "PyTis - NSIS Application Wizard"

name = AppWizard
version = Version
company = Powered By PyTis

written_by = """Written by Josh Lee %s 2004-2009.
All Rights Reserved.""" 

help = Help
close = Close
close_ = &Close


buttons.new = New
buttons.close = Close
buttons.load = Load
buttons.ok = &OK
buttons.done = Done
buttons.settings = Update Settings
buttons.save = Save
buttons.cancel = Cancel
buttons.vpatch = Create Patch
buttons.generate = Generate
buttons.defaults = Defaults
buttons.remove = &Remove
###############################################################################
#
# Tool Tips for Panel Buttons
#
tooltips.new = New
tooltips.vpatch = Generate Patch Installer 
tooltips.submit = Click here to Submit
tooltips.load = Load Project
tooltips.settings = Program Settings
tooltips.close = Close this Program
tooltips.save = Click here to Save Current Project
tooltips.cancel = Click here to Cancel
tooltips.done = Click here to return
tooltips.file_choose = Chose a file
tooltips.dir_choose = Chose a Folder
settings.tooltips.save = Save Settings
tooltips.generate = "Auto-Generate"
tooltips.defaults = Load Defaults


###############################################################################
# Error titles and messages
errors.default = ERROR
errors.complete = "Complete"
errors.comming_soon =  "Coming Soon,.."
errors.not_implemented = This feature is not yet implemented.
errors.success = Success
errors.sorry = "Sorry,..."
load.check = "Confirm"
load.check_remove = "Are you sure you wish to remove this item?"
errors.settings_updated = Settings updated Successfully.
errors.no_name = Please name your project.

errors.no_nsis = Please locate the makensisw.exe.
errors.invalid_nsis = Invalid NSIS file selected.
errors.nsis_path = NSIS file not found.
errors.file_not_found = "File not found."
errors.file_not_found_long = """Invalid file name, or file not found:
%s"""
errors.no_vpatch = Please locate the GenPat.exe.
errors.invalid_vpatch = Invalid vPatch file selected.
errors.vpatch_path = vPatch file not found.

errors.language = Invalid Language.
errors.config = "Configuration file corrupt."
errors.config_long = 'The config.ini Configuration file is unfortunately corrupt.  It has been saved as "config.ini.backup"' 
unknown = 'Un-Known'


errors.warning = "Warning"
warning.nsifile = "NSI file not found.  Either the path is wrong, or you haven't created it yet."
warning.overwrite = "This name has already been used, are you sure you want to over-write this file?"

load.buttons.cancel = &Cancel
load.errors.nofile = "Sorry,..."
load.errors.nofile_long = "No file selected"
python.errors.thread = Un-handled exception in thread

###############################################################################
## NSIS
walker.title = "PyTis.com NSIS Walker"
walker.buffer = Output Buffer
md5.title = "PyTis NSIS Walker - MD5"


walker.modes = Modes
walker.install = "Install Mode"
walker.uninstall = "Uninstall Mode"
walker.md5 = "MD5 Mode"

walker.options = "Options"
walker.debug = "Debug"
walker.force = "Force Delete (uninstall mode)"
walker.recursive = "Recursively Scan"
walker.instvar = Install Variable (default $INSTVAR)
walker.outfile = Write to file:
###############################################################################
# Base Panel
errors.missing_child_title = File not found
errors.missing_child = """Cannot locate program:
%s"""

main.title = Step One
main.name_name = Project Name:
main.project_name = PROJECT NAME
main.nsi_file = Installer *.nsi path
main.project_directory = Directory of current project
main.insh_file = Install *.nsh include file
main.unsh_file = Uninstall *.nsh include file
main.md5_file = md5 sum file (for patches)
###############################################################################
# Personal Settings Program
settings.nsis = NSIS "nsismakew.exe" path
settings.vpatch = vPatch "GenPat.exe" path
settings.default_language = Default Language:
main.help = Help


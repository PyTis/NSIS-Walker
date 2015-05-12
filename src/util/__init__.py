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
# Built In
import os, sys
import logging; log=logging.getLogger('util')
# Our Stuff

# 3rd Party

__all__ = ['base_dir',
           'default_dict',
           'mbool',
           'paths', 
           'remove_dir', 
           'show_error']

emergency_bug = [False]

def mbool(val, default=True):
    if not val:
        return False
    val = str(val).strip()
    if not val:
        return False
    if val.upper() in ['NONE', 'FALSE', '0']:
        return False
    if val.upper() in ['TRUE', '1', 'YES']:
        return True
    return default

class default_dict(dict):
    def __init__(self, other={}, default=None):
        dict.__init__(self, other)
        self.default = default
    
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self.default
        
base_dir = []


def get_base_dir():
    if not base_dir:
        if 'Console' in sys.argv[0]:
            base_dir.append(os.path.abspath(os.path.dirname(os.path.dirname(sys.argv[0]))))
        else:
            base_dir.append(os.path.abspath(os.path.dirname(sys.argv[0])))
    return base_dir[0]

def set_base_dir(b):
    base_dir = []
    base_dir.append(b)


def paths(base_dir=get_base_dir()):
    """
    Returns a dictionary with keys pointing to both relative and 
    locations for the program.
    """
    # WARNING ! DO NOT SAVE THESE PATHS TO CONFIG FILES!!!!
    # DRIVE LETTERS MAY CHANGE, MAKE SURE PATHS SAVED ARE RELATIVE!

    return {
        # REAL TIME PATHS
        'base_dir'     : base_dir,
        'settings_dir' : os.path.abspath(os.path.join(base_dir, 'lib', 'settings')),
        'language_dir' : os.path.abspath(os.path.join(base_dir, 'lib', 'settings/language')),
        # Actuall PC's path
                 
        
        # REAL TIME FILES
        'config'                : os.path.abspath(os.path.join(base_dir, 'lib', 'settings', 'config.ini')),
        'pin_pid'               : os.path.abspath(os.path.join(base_dir, 'lib', 'pin.pid')),

      
        # RELATIVE PATHS
        '_rel_settings_dir' : 'lib/settings',
           # RELATIVE FILES
    }

        

import wx

def show_error(err_name, err_msg, config, icon=wx.ICON_ERROR):
    """
    This is my nice helper method that makes displaying errors and notices
    that is much easier.
    """
  
    debug = mbool(config.get('debug','False'),False)
    supress_error_popups = mbool(config.get('supress_error_popups'), False)
    log.debug("debug: %s", debug)
    log.debug("supress_error_popups: %s", supress_error_popups)
    
    #from traceback import print_stack 
    if debug:
        log.info('-'*80)
        log.info('# Debugging popup stack trace DEBUG TRUE')
        log.info(err_msg)
        #log.info(print_stack())

    if not supress_error_popups:
        dlg = wx.MessageDialog(None, str(err_msg),
           str(err_name), wx.OK | icon
           )
        dlg.ShowModal()
        dlg.Destroy()
    # FOUND A VERY WEIRD BUG, see note *BUG1 at bottom
    return None

def _remove_files(start):
    """
    :start: a path
    Not used directly, but recursively removes files in a givin path.
    This is used by remove_dir
    """
    f=[]
    for root, dirs, files in os.walk(os.path.abspath(start), topdown=True):
        for name in files:
            fname = os.path.abspath(os.path.join(root,name))
            os.unlink(fname)
            
def remove_dir(start):
    """
    :start: a path
    Beats the windows OSError and IOError raised when trying to delete.
    This will recursively delete everything from start down, then 
    it will delete the start.
    """
    _remove_files(start)
    f=[]
    for root, dirs, files in os.walk(os.path.abspath(start), topdown=False):
        for name in dirs:
            fname = os.path.abspath(os.path.join(root,name))
            os.rmdir(fname)
    os.rmdir(start)

def verh(mylist):
    _o = []
    for outer in mylist:
        _i = ''
        for inner in str(outer):
            try: int(inner)
            except ValueError: pass
            else: _i+=str(inner)
        _o.append(_i)
    return _o
          
"""
* BUG 1
    Ok, so as we are adding buttons to our grid, they are laid out to display
    vertically, one below the next.  However, if the popup occurs, then they
    stack on top of each other.  The gridSizers don't work very well when 
    popups occur while adding the buttons to the grid.  Isn't that weird?
"""
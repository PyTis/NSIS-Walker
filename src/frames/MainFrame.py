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


# Our Stuff
from frames.BaseFrame import BaseFrame as BF
from panels.MainPanel import MainPanel as MP
from panels.Settings import Settings as SETTINGS
from util.language import language as LANG
import util as UTL
import util.images as IMG


# Third Party
import wx

__all__ = ['MainFrame']


class MainFrame(BF):
    Programs = None

    @property
    def bg_image(self):
        return IMG.getBackGroundBitmap() 
    
    def __init__(self, parent, title, pos=(-1,-1), size=(512,530)):
        
        self.parent = parent
        
        BF.__init__(self, parent, title, pos, size)


        try:
            self.SetIcon(IMG.getPytisIcon())
        finally:
            pass
        self.Show(False)
     
   
        self.Programs = MP(self) 
        self.Programs.Show(True)
        
        self.Settings = SETTINGS(self)
        self.Settings.Show(False)
        
        if UTL.emergency_bug[0]:
            UTL.show_error(LANG.lookup('errors.config'), 
                           LANG.lookup('errors.config_long'), 
                           self.config)
                           
        self.Show(True)
        
        
    def setup(self):
        pass

    def showSettings(self):
        self.Programs.Show(False)
        self.Settings.Show(True)
    def showPrograms(self):
        self.Programs.Show(True)
        self.Settings.Show(False)
        
    def CloseSelf(self):
        try:
            wx.Frame().Close(self)
        except TypeError:
            self.Destroy()
    
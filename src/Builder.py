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
import sys #importnanny os
# Our Stuff
from frames.MainFrame import MainFrame as Frame
import util as UTL
import util.app as AP
import util.configobj as COBJ
from util.language import language as LANG
# 3rd Party
import wx


ID_NEW = wx.NewId()
ID_OPEN = wx.NewId()
ID_SAVE = wx.NewId()


class MyApp(AP.App):

    def OnInit(self):
        frame =   self.f = Frame(None, LANG.lookup('title')) # debug from conf
        self.SetTopWindow(frame)

        print "Print statements go to this stdout window by default."

        frame.Show(True)
        return True


if __name__ == '__main__':
    

    config = COBJ.load(UTL.paths()['config'], True)
    DEBUG = UTL.mbool(config.get('debug','False'),False)

    if not DEBUG:
        # DEVELOPMENT MODE 1 of 2
        build = open("lib/logs/PyTis.exe.log", 'w+')
        sys.stdout = build
        
        
    app = MyApp(redirect=False, debug=DEBUG)
    app.MainLoop()


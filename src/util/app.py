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
#import os, sys
import cStringIO, subprocess, traceback #, time
# Our Stuff
import util as UTL
from util.language import language as LANG
from util import configobj as COBJ 
# 3rd Party
import wx


class MyIcon(wx.TaskBarIcon):
    pass


config = UTL.default_dict()


class App(wx.App):
    f = None # Frame
    _icon = None
    tooltip = None
    _config = {}
    looping = True

    def __init__(self, *args, **kwargs):
        self.debug = kwargs['debug']
        del kwargs['debug']
        wx.App.__init__(self, *args, **kwargs)
    ###########################################################################
    # Config
    
    @property
    def config(self):
        """ Non settable configuration object to live on the Application, and
            ONLY on the application.
        """
        if not self._config:
            self._config = COBJ.load(UTL.paths()['config'], True)
        if not self._config.get('projects'):
            self._config['projects'] = {}
            self._config.save()
        return self._config
    
    def save(self):
        self.config.save()
    ###########################################################################
    # Crud

    def _get_icon(self):
        return self._icon
    def _set_icon(self, icon):
        self._icon = icon
    icon = property(_get_icon, _set_icon)

    ###########################################################################
    # Mechanics
    def OnInit(self):
        #self.looping = True
        try:
            if self.icon:
                self.icon = MyIcon()
                self.icon.SetIcon(self.icon,self.tooltip)
                self.icon.Bind(wx.EVT_TASKBAR_LEFT_UP, self.Restore)
            self.run()

        except:
            self.OnException()
        return True

    def OnException(self):
        import logging as log
        data = cStringIO.StringIO()
        traceback.print_exc(file = data)
        if self.debug:
            print data.getvalue()
        else:
            log.error(data.getvalue())
        self.exit()
        
    def exit(self, event=None):
        try:
            if self.icon:
                self.icon.Destroy()
#            if log:
#                log.shutdown()
        except:
            self.looping = False
            self.OnException()

        self.looping = False
        return

    ###########################################################################
    # Wrappers
    def makeRun(self, path):
        cmd = '"%s"' % path
        def _(evt):
            try:
                return subprocess.Popen(args=cmd)
            except WindowsError, e:
                UTL.show_error(LANG.lookup('errors.default'),
                                "%s \n %s" %(str(e), cmd),
                                self.config,
                                wx.ICON_STOP)
        return _
    
    def browseAction(self, path):
        """
        Used as the action when the 'My Docs' Button is clicked on.
        """
        cmd = 'explorer.exe "%s"' % path
        def _(*notused):
            return subprocess.Popen(args=cmd)
        return _
    
    def makeChildProgram(self, path):
        """
        Used as the action when the 'My Docs' Button is clicked on.
        """
        def _(*notused):
            #self.Minimize(None)
            try:
                ret = subprocess.Popen(args=str(path))
            except:
                #self.Restore(None)
                UTL.show_error(LANG.lookup('errors.missing_child_title'),
                               LANG.lookup('errors.missing_child') % path,
                               wx.ICON_ERROR)
            #else:
            #    self.Restore(None)
        return _
    

            
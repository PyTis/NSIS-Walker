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
#from cStringIO import StringIO


# Our Stuff
from bin import app_walker
from dialogs.BaseDLG import BaseDLG

import util as UTL
import util.app as AP
import util.configobj as COBJ
import util.images as IMG

from util import mbool
#from util import my_button as BUTTONS
from util.language import language as LANG

# Third Party
import wx
import wx.lib.buttons  as  buttons

default_project = {
    'project_name' : '',
    'nsi_file'     : '',
    'insh_file'    : '_install.nsh',
    'unsh_file'    : '_uninstall.nsh',
    'md5_file'     : '_md5sum.txt',
    'project_dir'  : '',
    'install_var'  : '$INSTDIR',
    
}

class WalkerDLG(BaseDLG, wx.Frame):
    label = None
    config = {} # loaded in init


    @property
    def bg_image(self):
        return IMG.getDlgBGBitmap() 

    def _get_project(self):
        if not self._project:
            self._project = UTL.default_dict(other=default_project)
        return self._project
    def _set_project(self, project):
        self._project = UTL.default_dict(default_project)
        self._project.update(project)
    project = property(_get_project, _set_project)

    ##################################################################
    # Setup
    def setup(self):
     
       # font =  wx.Font(12, 12, wx.NORMAL, wx.BOLD, False, 'Sans')
        #self.labelx.font = font
        #self.labelx.color = "#0E253B"
        if self.Parent:
            self.project = self.Parent.project
      
        self.setCheckboxes()
        self.seDefaultsButton()
        self.setSaveButton()
        self.setCancelButton()
        self.setDoneButton()
        #self.value.SetFocus()
        self.setOutputFileBox()
        
        self.defaultsFromFile()
        
    def setCheckboxes(self):
        # force, all, # directory, iterate, install, un-install, -outfile, installvar, -debug, silent
        self.modes_lb = self.StaticText('walker.modes', (10,20))
        self.modes_lb.color = self.bt_fgcolor
        
        self.cb_install     = wx.RadioButton(self, -1, LANG.lookup('walker.install'), pos=(30, 40), style=wx.NO_BORDER)
        self.Bind(wx.EVT_RADIOBUTTON, self.onCBI, self.cb_install)
        
        self.cb_uninstall   = wx.RadioButton(self, -1, LANG.lookup('walker.uninstall'), pos=(225, 40), style=wx.NO_BORDER)
        self.Bind(wx.EVT_RADIOBUTTON, self.onCBU, self.cb_uninstall)
        
        self.cb_md5         = wx.RadioButton(self, -1, LANG.lookup('walker.md5'), pos=(385, 40), style=wx.NO_BORDER)
        self.Bind(wx.EVT_RADIOBUTTON, self.onCBM, self.cb_md5)
        
        self.options = self.StaticText('walker.options', (10,60))  
        self.options.color = self.bt_fgcolor
              
        self.cb_force       = wx.CheckBox(self, -1, LANG.lookup('walker.force'), pos=(30, 80), style=wx.NO_BORDER)
        self.Bind(wx.EVT_CHECKBOX, self.onCBF, self.cb_force)
        
        self.cb_recursive   = wx.CheckBox(self, -1, LANG.lookup('walker.recursive'), pos=(225, 80), style=wx.NO_BORDER)
        self.Bind(wx.EVT_CHECKBOX, self.onCBR, self.cb_recursive)
        
        self.cb_debug       = wx.CheckBox(self, -1, LANG.lookup('walker.debug'), pos=(385, 80), style=wx.NO_BORDER)
        self.Bind(wx.EVT_CHECKBOX, self.onCBD, self.cb_debug)

    def onCBI(self, e):
        self.outfile.SetValue(self.getOutFile())
        self.config['walker_options']['-m0'] = True
        self.config['walker_options']['-m1'] = False
        self.config['walker_options']['-m2'] = False
        self.config.save()

    def onCBU(self, e):
        self.outfile.SetValue(self.getOutFile())
        self.config['walker_options']['-m0'] = False
        self.config['walker_options']['-m1'] = True
        self.config['walker_options']['-m2'] = False
        self.config.save()

    def onCBM(self, e):
        self.outfile.SetValue(self.getOutFile())
        self.config['walker_options']['-m0'] = False
        self.config['walker_options']['-m1'] = False
        self.config['walker_options']['-m2'] = True
        self.config.save()

    def onCBF(self, e):
   
        self.config['walker_options']['-F'] = e.IsChecked()
        self.config.save()

    
    def onCBR(self, e):
     
        self.config['walker_options']['-i'] = e.IsChecked()
        self.config.save()


    def onCBD(self, e):
     
        self.config['walker_options']['-D'] = e.IsChecked()
        self.config.save()

    
    def setOutputFileBox(self):
        self.vlabel = self.StaticText('walker.inst_var', (170,100))
       # self.vlabel.color = self.bt_fgcolor
        
        self.inst_var = wx.TextCtrl(self, -1, self.project.get('inst_var',''), size=(130,-1),
                                     pos=(30,98))

    
        self.olabel = self.StaticText('walker.outfile', (30,125))
        self.outfile = wx.TextCtrl(self, -1, 'langauge', size=(425,-1),
                                     pos=(40,144))
      
        
        self.plabel = self.StaticText('walker.buffer', (30,170))
        self.value = wx.TextCtrl(self, -1, '', size=(425,250),
                                       pos=(40,190),
                                       style=wx.VSCROLL
                                       |wx.TE_READONLY
                                       |wx.TE_MULTILINE )


        #self.value.LoadFile(buf.getvalue())
        #self.value.Disable()

       # self.Bind(wx.EVT_TEXT_ENTER, self.EndModal, self.value)                             

    def getOutFile(self):
        parent_folder = os.path.abspath(self.project['project_dir']) or os.path.abspath(os.curdir())
        if self.cb_install.Value:
            return self.Parent.insh_file.GetValue()
            if self.project['insh_file'] and self.project['insh_file'] !=  default_project['insh_file']:
                retval = self.project['insh_file']
            else:
                retval = os.path.abspath(os.path.join(parent_folder, "%s%s" % \
                                                      (self.project['project_name'].replace(' ','_'), default_project['insh_file'])))
        if self.cb_uninstall.Value:
            return self.Parent.unsh_file.GetValue()
            if self.project['unsh_file'] and self.project['unsh_file'] !=  default_project['unsh_file']:
                retval = self.project['unsh_file']
            else:
                retval = os.path.abspath(os.path.join(parent_folder, "%s%s" % \
                                                      (self.project['project_name'].replace(' ','_'), default_project['unsh_file'])))
        if self.cb_md5.Value:
            return self.Parent.md5_file.GetValue()
            if self.project['md5_file'] and self.project['md5_file'] !=  default_project['md5_file']:
                retval = self.project['md5_file']
            else:
                retval = os.path.abspath(os.path.join(parent_folder, "%s%s" % \
                                                      (self.project['project_name'].replace(' ','_'), default_project['md5_file'])))            
     
        return retval 


    def seDefaultsButton(self):
        self.defaults_button = buttons.GenButton(self, -1, 'language',
                                    pos=(400,5),
                                    style=wx.BORDER_NONE&wx.BU_AUTODRAW)
          
        LANG.addButton(self.defaults_button, 'buttons.defaults', 'tooltips.defaults')
        self.Bind(wx.EVT_BUTTON, self.onLoadDefaults, self.defaults_button)
        self.colorBtn(self.defaults_button)
        
    def setSaveButton(self):
        self.save_button = buttons.GenButton(self, -1, 'language',
                                    pos=(400,450),
                                    style=wx.BORDER_NONE&wx.BU_AUTODRAW)
          
        LANG.addButton(self.save_button, 'buttons.generate', 'tooltips.generate')
        self.Bind(wx.EVT_BUTTON, self.onGenerate, self.save_button)
        self.colorBtn(self.save_button)
        
    def setCancelButton(self):
        self.cancel_button = buttons.GenButton(self, wx.ID_CANCEL, 'language',
                                    pos=(40,450),
                                    style=wx.BORDER_NONE&wx.BU_AUTODRAW)
          
        LANG.addButton(self.cancel_button, 'buttons.cancel', 'tooltips.cancel')
        self.Bind(wx.EVT_BUTTON, self.EndModal, self.cancel_button)
        self.colorBtn(self.cancel_button)
        
    def setDoneButton(self):
        self.done_button = buttons.GenButton(self, wx.ID_CANCEL, 'language',
                                    pos=(40,450),
                                    style=wx.BORDER_NONE&wx.BU_AUTODRAW)
          
        LANG.addButton(self.done_button, 'buttons.done', 'tooltips.done')
        self.Bind(wx.EVT_BUTTON, self.EndModal, self.done_button)
        self.colorBtn(self.done_button)
        self.done_button.Show(False)

    def defaultsFromFile(self):
        self.cb_debug.SetValue(mbool(self.config['walker_options']['-D']))
        self.cb_force.SetValue(mbool(self.config['walker_options']['-F']))
        self.cb_install.SetValue(mbool(self.config['walker_options']['-m0']))
        self.cb_uninstall.SetValue(mbool(self.config['walker_options']['-m1']))
        self.cb_md5.SetValue(mbool(self.config['walker_options']['-m2']))
        self.cb_recursive.SetValue(mbool(self.config['walker_options']['-i']))
        self.inst_var.SetValue(default_project['install_var'])
        self.outfile.SetValue(self.getOutFile())
        
    def onLoadDefaults(self, event):
        self.setDefaults()
        self.defaultsFromFile()
        event.Skip()
        
    ##################################################################
    # Wrappers
    def GetValue(self):
        return self.value.GetValue()

    #################################################################
    # Buttons Events.

    def EndModal(self, event):
        id = event.GetId()
        if id != wx.ID_OK and id != wx.ID_CANCEL:
            return

        if __name__ == '__main__':
            try:   
                wx.GetApp().exit(event)
            except:
                wx.GetApp().destroy()
            else:
                sys.exit(0)
                
        return wx.Dialog.EndModal(self, id)
    ##################################################################
    # Mechanics
    def onGenerate(self, event):
        self.value.SetValue('')
        opts = UTL.default_dict()
        opts.all = False
        opts.debug = self.cb_debug.GetValue() #(mbool(self.config['walker_options']['-D']))
        opts.force = self.cb_force.GetValue() #(mbool(self.config['walker_options']['-F']))
        opts.iterate = not self.cb_recursive.GetValue()
        if self.cb_install.GetValue(): #(mbool(self.config['walker_options']['-m0']))
            opts.mode = '0'
        elif self.cb_uninstall.GetValue(): #(mbool(self.config['walker_options']['-m1']))
            opts.mode = '1'
        elif self.cb_md5.GetValue(): #(mbool(self.config['walker_options']['-m2']))
            opts.mode = '2'
        opts.instvar = self.inst_var.GetValue().strip() #(default_project['install_var'])
        opts.directory = self.project['project_dir']
        opts.outfile = None
        opts.handle = file(self.outfile.GetValue(), 'w')
        
        app_walker.mode(opts)
        handle = file(self.outfile.GetValue(), 'r')
        for line in handle.readlines(-1):
            self.value.write(line)
            self.value.SetInsertionPointEnd()
        self.cancel_button.Show(False)
        self.done_button.Show(True)
   
        #self.outfile.GetValue() #(self.getOutFile())

class MyApp(AP.App):

    def OnInit(self):
        dlg =   self.D = WalkerDLG(None, -1,
                                   LANG.lookup('walker.title')) # debug from conf

        self.SetTopWindow(dlg)

        dlg.Show(True)
        return True


if __name__ == '__main__':

    
    config = COBJ.load(UTL.paths()['config'], True)
    DEBUG = UTL.mbool(config.get('debug','False'),False)
    print DEBUG
    if not DEBUG:
        # DEVELOPMENT MODE 1 of 2
        build = open("lib/logs/PyTis.exe.log", 'w+')
        sys.stdout = build
        
        
    app = MyApp(redirect=False, debug=DEBUG)
    app.MainLoop()
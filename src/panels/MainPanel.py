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
import datetime, os, subprocess#, sys

# Our Stuff
from dialogs.WalkerDLG import WalkerDLG
from dialogs.LoadDLG import LoadDLG
from panels.BasePanel import BasePanel as BasePanel
import util as UTL
from util.language import language as LANG
from util import my_button as BUTTONS
import util.images as IMG
#import util.my_button as MYBUT

import logging; log=logging.getLogger('MainPanel')
# Third Party
import wx
import wx.lib.buttons  as  buttons

__all__ = ['NSISMainAppPanel']



class ValidationError(Exception):
    pass


default_project = {
    'project_name' : '',
    'nsi_file'     : '',
    'insh_file'    : '_install.nsh',
    'unsh_file'    : '_uninstall.nsh',
    'md5_file'     : '_md5sum.txt',
    'project_dir'  : '',
    'install_var'  : '$INSTDIR',
    
}

class MainPanel(BasePanel):
    """
    Sencd all of our panes will have much in common
    I figure it would be best to make a parent class
    to simply override, so there won't be so much 
    duplicate code.
    """
   
    data = {}
    xpos = 26
    ypos = 56
    _project = {}
    
    def _get_project(self):
        if not self._project:
            self._project = UTL.default_dict(other=default_project)
        return self._project
    def _set_project(self, project):
        self._project = UTL.default_dict(default_project)
        self._project.update(project)
    project = property(_get_project, _set_project)

    @property
    def bg_image(self):
        return IMG.getProgramBitmap() #IMG.getBackGroundBitmap() 



    def setup(self):
        """
        To make our init less complicated this calls the methods that draw
        the default background stuff on our panes.  This can be overridden
        in the future to not show some of the features below, however 
        you should use when if you do are still going to leave
        everything below running.
        """
        if self.config.get('last_project'):
            try:
                self.project = self.config['projects'][self.config['last_project'].strip()]
            except KeyError, e:
                pass
        
        self.setTitle()
        self.setSettingButton()
        self.setPatchButton()
        
        self.setNameBox()
        self.drawBar()
        
        self.setDirectoryBox()
        self.setProjectDirButton()
        self.drawBar()
        
        self.setNSIFileButton()
        self.setNSIFileBox()
        self.drawBar()
        
        self.setInstallNSHFileBox()
        self.setInstallNSHFile()
        self.setGenerateINSH()
        
        
        self.setUninstallNSHFileBox()
        self.setUninstallNSHFile()
        self.setGenerateUNSH_Button()
        
        self.setMd5FileBox()
        self.setMd5File()
        self.setGenerateMD5_Button()
        
        #self.drawBar()
        self.setNewButton()
        self.setLoadButton() 
        self.setSaveButton()
        
         
    ###########################################################################
    # Setup methods
    def setTitle(self):
        labelx = self.StaticText('title', (60,14))
        font =  wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD, False, 'Sans')
        labelx.font = font
        labelx.color = self.fgcolor

        
    def setNameBox(self):
        xa,ya,xb,yb= self.getPos(); self.StaticText('main.name_name', (xa,ya))
        self.name_box = wx.TextCtrl(self, -1, self.project.get('project_name',''), size=(175,-1),pos=(xb,yb))
       
        
    def setDirectoryBox(self):
        xa,ya,xb,yb= self.getPos(); self.StaticText('main.project_directory', (xa,ya))
        self.project_dir = wx.TextCtrl(self, -1, self.project.get('project_dir',''), size=(375,-1), pos=(xb,yb))
      
        
    def setNSIFileBox(self):
        xa,ya,xb,yb= self.getPos(); self.StaticText('main.nsi_file', (xa,ya))
        self.nsi_file = wx.TextCtrl(self, -1, self.project.get('nsi_file',''), size=(375,-1), pos=(xb,yb))

 
    def setInstallNSHFileBox(self):
        xa,ya,xb,yb= self.getPos(); self.StaticText('main.insh_file', (xa,ya))
        self.insh_file = wx.TextCtrl(self, -1, self.project.get('insh_file',''), size=(375,-1),pos=(xb,yb))
  
        
    def setUninstallNSHFileBox(self):
        xa,ya,xb,yb= self.getPos(); self.StaticText('main.unsh_file', (xa,ya))
        self.unsh_file = wx.TextCtrl(self, -1, self.project.get('unsh_file',''), size=(375,-1),pos=(xb,yb))

        
    def setMd5FileBox(self):
        xa,ya,xb,yb= self.getPos(); self.StaticText('main.md5_file', (xa,ya))
        self.md5_file = wx.TextCtrl(self, -1, self.project.get('md5_file',''), size=(375,-1),pos=(xb,yb))

    ##################################################################
    # Create Buttons
    def onGenInsh(self,e):
        if not self.insh_file.GetValue().endswith('.nsh') or \
        os.path.isdir(os.path.abspath(self.insh_file.GetValue())):
            return UTL.show_error(LANG.lookup('errors.file_not_found '),
                           LANG.lookup('errors.file_not_found_long') % self.insh_file.GetValue(),
                           self.config)
            
        self.config['walker_options']['-m0'] = True
        self.config['walker_options']['-m1'] = False
        self.config['walker_options']['-m2'] = False
        self.config.save()
        dlg = WalkerDLG(self, -1, LANG.lookup('insh.title'))
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()
        
    def onGenUnsh(self,e):
        if not self.unsh_file.GetValue().endswith('.nsh') or \
        os.path.isdir(os.path.abspath(self.unsh_file.GetValue())):
            return UTL.show_error(LANG.lookup('errors.file_not_found '),
                           LANG.lookup('errors.file_not_found_long') % self.unsh_file.GetValue(),
                           self.config)
            
        self.config['walker_options']['-m0'] = False
        self.config['walker_options']['-m1'] = True
        self.config['walker_options']['-m2'] = False
        self.config.save()
        dlg = WalkerDLG(self, -1, LANG.lookup('unsh.title'))
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()
    def onGenMD5(self,e):

        if not self.md5_file.GetValue().endswith('md5sum.txt') or \
        os.path.isdir(os.path.abspath(self.md5_file.GetValue())):
            return UTL.show_error(os.path.isdir(os.path.abspath(self.md5_file.GetValue())),
                           LANG.lookup('errors.file_not_found_long') % self.md5_file.GetValue(),
                           self.config)
            
        self.config['walker_options']['-m0'] = False
        self.config['walker_options']['-m1'] = False
        self.config['walker_options']['-m2'] = True
        self.config.save()

        dlg = WalkerDLG(self, -1, LANG.lookup('md5.title'))
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()
   
        
    def setSettingButton(self):
        self.settings_bttn = self.makeMyImageButton(IMG.getSettingsBttnBitmap(), pos=(460,5),tooltip='tooltips.settings',event_handler=self.onShowSettings)
    def setProjectDirButton(self):
        self.project_dir_bttn = self.makeMyImageButton(IMG.getDirBitmap(), pos=(410,144),tooltip='main.project_directory',event_handler=self.onProjectPath)
    def setNSIFileButton(self):
        self.nsi_file_bttn = self.makeMyImageButton(IMG.getDirBitmap(),pos=(410,218),tooltip='main.nsi_file',event_handler=self.onNSIPath)
    
    # INSH   
    def setInstallNSHFile(self): self.insh_file_bttn = self.makeMyImageButton(IMG.getDirBitmap(),pos=(410,290),tooltip='main.insh_file',event_handler=self.onInshPath)
    def setUninstallNSHFile(self): self.unsh_file_bttn = self.makeMyImageButton(IMG.getDirBitmap(),pos=(410,326),tooltip='main.unsh_file',event_handler=self.onUnshPath)
    def setMd5File(self): self.md5_file_bttn = self.makeMyImageButton(IMG.getDirBitmap(),pos=(410,360),tooltip='main.md5',event_handler=self.onMd5Path)

    def setGenerateINSH(self):
        self.gnsh_file_bttn = self.makeMyImageButton(IMG.getWindowButtonBitmap(),(438,290),'tooltips.generate',self.onGenInsh)

    def setGenerateUNSH_Button(self): 
        self.gunsh_file_bttn = self.makeMyImageButton(IMG.getWindowButtonBitmap(),(438,326),'tooltips.generate',self.onGenUnsh)
        
    def setGenerateMD5_Button(self):
        self.gmd5_file_bttn = self.makeMyImageButton(IMG.getWindowButtonBitmap(),(438,360),'tooltips.generate',self.onGenMD5)
        

        
    def makeMyImageButton(self, image, pos, tooltip, event_handler, size=(24,24), event=wx.EVT_BUTTON):
        button = BUTTONS.PicButton(self,-1, image, pos=pos, size=size)
        LANG.addButtonTooltip(button, tooltip)
        button.SetBitmapDisabled(image)
        button.SetBitmapHover(image)
        button.SetBitmapFocus(image)        
        button.SetBitmapSelected(image)
        button.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        self.Bind(event, event_handler, button)
        

    def setNewButton(self):
        self.new_button = buttons.GenButton(self, -1, 'language',
                                    pos=(150,450),
                                    style=wx.BORDER_NONE&wx.BU_AUTODRAW)
          
        LANG.addButton(self.new_button, 'buttons.new', 'tooltips.new')
        self.Bind(wx.EVT_BUTTON, self.onNew, self.new_button)
        self.colorBtn(self.new_button)
        
    def setLoadButton(self):
        self.load_button = buttons.GenButton(self, -1, 'language',
                                    pos=(275,450),
                                    style=wx.BORDER_NONE&wx.BU_AUTODRAW)
          
        LANG.addButton(self.load_button, 'buttons.load', 'tooltips.load')
        self.Bind(wx.EVT_BUTTON, self.onLoad, self.load_button)
        self.colorBtn(self.load_button)

        
    def setPatchButton(self):
        self.patch_button = buttons.GenButton(self, -1, 'language',
                                    pos=(208,73),
                                    style=wx.BORDER_NONE&wx.BU_AUTODRAW)
          
        LANG.addButton(self.patch_button, 'buttons.vpatch', 'tooltips.vpatch')
        self.Bind(wx.EVT_BUTTON, self.futureFeature, self.patch_button)
        self.colorBtn(self.patch_button)
        
        
    def setSaveButton(self):
        self.save_button = buttons.GenButton(self, -1, 'language',
                                    pos=(400,450),
                                    style=wx.BORDER_NONE&wx.BU_AUTODRAW)
          
        LANG.addButton(self.save_button, 'buttons.save', 'tooltips.save')
        self.Bind(wx.EVT_BUTTON, self.onSave, self.save_button)
        self.colorBtn(self.save_button)
    ##################################################################
    # Mechanics

    def drawBar(self):
        xa,ya,xb,yb= self.getPos()
        line = wx.StaticLine(self, -1, pos=(xb,yb), size=(175,2), style=wx.LI_HORIZONTAL )
        
    def getOptions(self):
        options = []
        for name, proj in self.config.get('projects', {}).items():
            try:
                ddate = self.config['projects'][name]['display_date']
            except KeyError, e:
                ddate = "Date Missing"
            options.append((name, ddate))
        return options    
            
    def load(self, project_name):
        try:
            self.project = self.config['projects'][project_name]
            self.name_box.SetValue(self.project['project_name'])
            self.project_dir.SetValue(self.project['project_dir'])
            self.nsi_file.SetValue(self.project['nsi_file'])
            self.insh_file.SetValue(self.project['insh_file'])
            self.unsh_file.SetValue(self.project['unsh_file'])
            self.md5_file.SetValue(self.project['md5_file'])
        except KeyError, e:
            raise KeyError, e
            
        else:
            self.config['last_project'] = project_name
            self.config.save()

    ##################################################################
    # Button Events.
    def onLoad(self, evt):

        dlg = LoadDLG(parent=self,
                      id=-1,
                      title='title',
                      options=self.getOptions(), 
                      name='name',
                      config=self.config)
        dlg.ShowModal()
        dlg.Destroy()
        

    def onNew(self,e):
        self.project = default_project
        self.name_box.SetValue('')
        self.project_dir.SetValue('')
        self.nsi_file.SetValue('')
        self.insh_file.SetValue(self.project['insh_file'])
        self.unsh_file.SetValue(self.project['unsh_file'])
        self.md5_file.SetValue(self.project['md5_file'])
        
    def onSave(self, evt):
        data = {'project_name'  : self.name_box.GetValue(),
                'nsi_file'      : self.nsi_file.GetValue(),
                'insh_file'     : self.insh_file.GetValue(),
                'unsh_file'     : self.unsh_file.GetValue(),
                'md5_file'      : self.md5_file.GetValue(),
                'project_dir'   : self.project_dir.GetValue(),
                'saved_date'    : datetime.datetime.now(),
                'display_date'  : datetime.datetime.now().strftime("%I:%M%%s %m %b, %Y") % datetime.datetime.now().strftime("%p").lower(),
                'inst_var'      : self.project['install_var']
        }
        try:
            data = self.validate(data)
            if not data:
                return
        except ValidationError, e:
            return UTL.show_error(LANG.lookup('errors.sorry'),
                                   str(e),
                                   self.config,
                                   wx.ICON_EXCLAMATION)
        else:
            self.save(data)
            
            
    def onNSIPath(self, evt):
        if self.nsi_file.GetValue() and os.path.exists(os.path.dirname(self.nsi_file.GetValue())):
            default_dir = os.path.dirname(self.nsi_file.GetValue())
        elif self.project['project_dir'] and os.path.isdir(self.project['project_dir']):
            default_dir = self.project['project_dir']
        else:
            default_dir = os.getcwd()
        
        dlg = wx.FileDialog(
            self, message=LANG.lookup('tooltips.file_choose'),
            defaultDir=default_dir,
            defaultFile="",
            wildcard="NSI File (*.nsi)|*.nsi|",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                if path.lower().endswith('.nsi'):
                    self.nsi_file.SetValue(os.path.abspath(path))
        dlg.Destroy()
        
    def onInshPath(self,e):
        if self.insh_file.GetValue() and os.path.exists(os.path.dirname(self.insh_file.GetValue())):
            default_dir = os.path.dirname(self.insh_file.GetValue())
        elif self.project['project_dir'] and os.path.isdir(self.project['project_dir']):
            default_dir = self.project['project_dir']
        else:
            default_dir = os.getcwd()
        
        dlg = wx.FileDialog(
            self, message=LANG.lookup('tooltips.file_choose'),
            defaultDir=default_dir,
            defaultFile="",
            wildcard="NSH include File (*.nsh)|*.nsh|",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                if path.lower().endswith('.nsh'):
                    self.insh_file.SetValue(os.path.abspath(path))
        dlg.Destroy()
    
    
    def onUnshPath(self,e):
        if self.unsh_file.GetValue() and os.path.exists(os.path.dirname(self.unsh_file.GetValue())):
            default_dir = os.path.dirname(self.unsh_file.GetValue())
        elif self.project['project_dir'] and os.path.isdir(self.project['project_dir']):
            default_dir = self.project['project_dir']
        else:
            default_dir = os.getcwd()
        
        dlg = wx.FileDialog(
            self, message=LANG.lookup('tooltips.file_choose'),
            defaultDir=default_dir,
            defaultFile="",
            wildcard="NSH include File (*.nsh)|*.nsh|",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                if path.lower().endswith('.nsh'):
                    self.unsh_file.SetValue(os.path.abspath(path))
        dlg.Destroy()
        
    def onMd5Path(self,e):
        if self.md5_file.GetValue() and os.path.exists(os.path.dirname(self.md5_file.GetValue())):
            default_dir = os.path.dirname(self.md5_file.GetValue())
        elif self.project['project_dir'] and os.path.isdir(self.project['project_dir']):
            default_dir = self.project['project_dir']
        else:
            default_dir = os.getcwd()
        
        dlg = wx.FileDialog(
            self, message=LANG.lookup('tooltips.file_choose'),
            defaultDir=default_dir,
            defaultFile="",
            wildcard="Auto-Generated (*md5sum.txt)|*md5sum.txt|",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                if path.lower().endswith('md5sum.txt'):
                    self.md5_file.SetValue(os.path.abspath(path))
        dlg.Destroy()
        
    def onProjectPath(self, evt):
        if self.project_dir.GetValue() and os.path.exists(os.path.dirname(self.project_dir.GetValue())):
            default_dir = os.path.dirname(self.project_dir.GetValue())
        elif self.project['project_dir'] and os.path.isdir(self.project['project_dir']):
            default_dir = self.project['project_dir']
        else:
            default_dir = os.getcwd()
        
        dlg = wx.DirDialog(
            self, message=LANG.lookup('tooltips.dir_choose'),
            defaultPath=default_dir, 
            style=wx.DD_DEFAULT_STYLE
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if os.path.isdir(path):
                self.project_dir.SetValue(os.path.abspath(path))
        dlg.Destroy()
    ##################################################################
    # Helpers
        
    def getPos(self):
        group = self.xpos, self.ypos+2, self.xpos, self.ypos+18
        self.ypos += 36
        return group
    
    def makeRun(self, path):
        cmd = '"%s"' % path
        def _(evt):
            try:
                return subprocess.Popen(args=cmd)
            except WindowsError, e:
                UTL.show_error("ERROR", "%s \n %s" %(str(e), cmd), wx.ICON_STOP)
        return _
    
    ##################################################################
    # Record Handling

    def validate(self, data):
        """
        :data: config record, almost, this method makes some changes.
        
        Validates the config record
        Rraises error if their is a problem with it.
        MAKES CHANGES TO RECORD
        RETURNS updated record, ready to be saved.
        
        """

        if not data['project_name'].strip():
            raise ValidationError, LANG.lookup('errors.no_name')
    
        if data['project_name'] != self.project.get('project_name'): # it has changed
                if data['project_name'] in self.config.get('projects'): # and that name is used
                    
                    dlg = wx.MessageDialog(self, message=LANG.lookup('warning.overwrite'),
                       caption=LANG.lookup('errors.warning'), style= wx.YES_NO| wx.ICON_QUESTION
                       )
                    if dlg.ShowModal() == wx.ID_YES:
                        pass
                    else:
                        self.name_box.SetValue(self.project.get('project_name',''))
                        return False
                    dlg.Destroy()
 
        if not os.path.isfile(os.path.abspath(data['nsi_file'])):
            UTL.show_error(LANG.lookup('errors.warning'),
                                      LANG.lookup('warning.nsifile'),
                                      self.config,
                                      wx.ICON_INFORMATION)
       
        return data
    
    def save(self, data):
        # Language stuff
        self.project = data
        name = self.project['project_name'].strip()
        self.config['last_project'] = name
        self.config['projects'][name] = data
        self.name_box.SetFocusFromKbd()
        self.name_box.SetInsertionPointEnd()
        return self.config.save()
        
    
        
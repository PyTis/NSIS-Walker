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
import os, subprocess#, sys

# Our Stuff
from panels.BasePanel import BasePanel as BasePanel
from util.language import language as LANG
from util.language import languages, LanguageError
import util as UTL
from util import my_button as BUTTONS
#import util.my_button as MYBUT
import util.images as IMG

# Third Party
import wx
import wx.lib.buttons  as  buttons

import logging; log=logging.getLogger('Settings')

__all__ = ['NSISMainAppPanel']


class ValidationError(Exception):
    pass



class Settings(BasePanel):
    """
    Sencd all of our panes will have much in common
    I figure it would be best to make a parent class
    to simply override, so there won't be so much 
    duplicate code.
    """
   
    data = {}
    xpos = 26
    ypos = 56

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
        self.setTitle()
        self.setUpdateButton()
       # self.setCloseButton()
        
        self.setNSISBox()
        self.setNSISDirButton()
        self.drawBar()
        
        self.setVPATCHBox()
        self.setVpatchDirButton()
        self.drawBar()
        
        self.setLanguageBox()

        self.setSaveButton()
        self.nsis_path.SetFocus()
        print self.config
        
    ###########################################################################
    # Setup methods
    def setTitle(self):
        labelx = self.StaticText('title', (60,14))
        font =  wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD, False, 'Sans')
        labelx.font = font
        labelx.color = self.fgcolor

    def setNSISBox(self):
        xa,ya,xb,yb= self.getPos()
        self.StaticText('settings.nsis', (xa,ya))

        self.nsis_path = wx.TextCtrl(self, -1, 'langauge', size=(375,-1),
                                     pos=(xb,yb))
        LANG.addTextCtrl(self.nsis_path, self.config, "nsis_path", '')
        
    def setVPATCHBox(self):
        xa,ya,xb,yb= self.getPos()
        self.StaticText('settings.vpatch', (xa,ya))

        self.vpatch_path = wx.TextCtrl(self, -1, 'langauge', size=(375,-1),
                                     pos=(xb,yb))
        LANG.addTextCtrl(self.vpatch_path, self.config, "vpatch_path", '')


    def setLanguageBox(self):
        xa,ya,xb,yb= self.getPos()
        self.StaticText('settings.default_language', (xa,ya))
        self.language = wx.ComboBox(self, -1, self.config.get("language", ''),
                                    size=(175,-1), pos=(xb,yb),
                                     choices=languages.keys())
    ##################################################################
    # Buttons Events.
    def setCloseButton(self):
        self.close_bttn = BUTTONS.PicButton(self,-1,
                              IMG.getCloseNotActiveBitmap(),
                              pos=(450,5),
                              size=(26,26))
        LANG.addButtonTooltip(self.close_bttn, 'tooltips.close')
        self.close_bttn.SetBitmapDisabled(IMG.getBttnDissabledBitmap())
        self.close_bttn.SetBitmapHover(IMG.getCloseBitmap())
        self.close_bttn.SetBitmapFocus(IMG.getCloseBitmap())        
        self.close_bttn.SetBitmapSelected(IMG.getCloseActiveBitmap())
        self.close_bttn.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        self.Bind(wx.EVT_BUTTON, self.onCloseFrame, self.close_bttn)


    def setUpdateButton(self):
        self.settings_bttn = BUTTONS.PicButton(self,-1,
                              IMG.getUpdateNotActiveBitmap(),
                              pos=(460,5),
                              size=(26,26))
        LANG.addButtonTooltip(self.settings_bttn, 'tooltips.settings')
        self.settings_bttn.SetBitmapDisabled(IMG.getBttnDissabledBitmap())
        self.settings_bttn.SetBitmapHover(IMG.getUpdateBitmap())
        self.settings_bttn.SetBitmapFocus(IMG.getUpdateBitmap())        
        self.settings_bttn.SetBitmapSelected(IMG.getUpdateActiveBitmap())
        self.settings_bttn.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        self.Bind(wx.EVT_BUTTON, self.onShowPrograms, self.settings_bttn)


    def setSaveButton(self):
        self.save_button = buttons.GenButton(self, -1, 'language',
                                    pos=(400,400),
                                    style=wx.BORDER_NONE&wx.BU_AUTODRAW)
          
        LANG.addButton(self.save_button, 'buttons.settings', 'settings.tooltips.save')
        self.Bind(wx.EVT_BUTTON, self.onSave, self.save_button)
        self.colorBtn(self.save_button)
        
    def setNSISDirButton(self):
        self.nsis_dir_bttn = BUTTONS.PicButton(self,-1,
                              IMG.getDirBitmap(),
                              pos=(410,74),
                              size=(24,24))
        LANG.addButtonTooltip(self.nsis_dir_bttn, 'tooltips.close')
        self.nsis_dir_bttn.SetBitmapDisabled(IMG.getDirBitmap())
        self.nsis_dir_bttn.SetBitmapHover(IMG.getDirBitmap())
        self.nsis_dir_bttn.SetBitmapFocus(IMG.getDirBitmap())        
        self.nsis_dir_bttn.SetBitmapSelected(IMG.getDirBitmap())
        self.nsis_dir_bttn.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        self.Bind(wx.EVT_BUTTON, self.onNSISPath, self.nsis_dir_bttn)

    def setVpatchDirButton(self):
        self.vpatch_dir_bttn = BUTTONS.PicButton(self,-1,
                              IMG.getDirBitmap(),
                              pos=(410,145),
                              size=(24,24))
        LANG.addButtonTooltip(self.vpatch_dir_bttn, 'tooltips.close')
        self.vpatch_dir_bttn.SetBitmapDisabled(IMG.getDirBitmap())
        self.vpatch_dir_bttn.SetBitmapHover(IMG.getDirBitmap())
        self.vpatch_dir_bttn.SetBitmapFocus(IMG.getDirBitmap())        
        self.vpatch_dir_bttn.SetBitmapSelected(IMG.getDirBitmap())
        self.vpatch_dir_bttn.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        self.Bind(wx.EVT_BUTTON, self.onGenPatPath, self.vpatch_dir_bttn)



    ##################################################################
    # Mechanics

    def drawBar(self):
        xa,ya,xb,yb= self.getPos()
        line = wx.StaticLine(self, -1, pos=(xb,yb), size=(175,2),
                             style=wx.LI_HORIZONTAL )
        
    def onSave(self, evt):
        data = {'nsis_path' : self.nsis_path.GetValue(),
                'vpatch_path' : self.vpatch_path.GetValue(),
                'language' : self.language.GetValue(),
        }
        try:
            data = self.validate(data)
        except ValidationError, e:
            return UTL.show_error(LANG.lookup('errors.sorry'),
                                   str(e),
                                   self.config,
                                   wx.ICON_EXCLAMATION)
        else:
            self.save(data)
            
    def onGenPatPath(self, evt):
        if self.vpatch_path.GetValue() and os.path.exists(os.path.dirname(self.vpatch_path.GetValue())):
            default_dir = os.path.dirname(self.vpatch_path.GetValue())
        else:
            default_dir = os.getcwd()
        
        dlg = wx.FileDialog(
            self, message=LANG.lookup('tooltips.file_choose'),
            defaultDir=default_dir,
            defaultFile="",
            wildcard="vPatch (GenPat.exe)|GenPat.exe|",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                if path.lower().endswith('genpat.exe'):
                    self.vpatch_path.SetValue(os.path.abspath(path))
        dlg.Destroy()
        
    def onNSISPath(self, evt):
        if self.nsis_path.GetValue() and os.path.exists(os.path.dirname(self.nsis_path.GetValue())):
            default_dir = os.path.dirname(self.nsis_path.GetValue())
        else:
            default_dir = os.getcwd()
        
        dlg = wx.FileDialog(
            self, message=LANG.lookup('tooltips.file_choose'),
            defaultDir=default_dir, 
            defaultFile="",
            wildcard="MakeNSIS (makensisw.exe)|makensisw.exe|",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                if path.lower().endswith('makensisw.exe'):
                    self.nsis_path.SetValue(os.path.abspath(path))
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
        
   
        if not data['nsis_path'].strip():
            raise ValidationError, LANG.lookup('errors.no_nsis')
        if not data['nsis_path'].lower().endswith('makensisw.exe'):
            raise ValidationError, LANG.lookup('errors.invalid_nsis')
        if not os.path.isfile(data['nsis_path']):
            raise ValidationError, LANG.lookup('errors.nsis_path')
      
        if not data['vpatch_path'].strip():
            raise ValidationError, LANG.lookup('errors.no_vpatch')
        if not data['vpatch_path'].lower().endswith('genpat.exe'):
            raise ValidationError, LANG.lookup('errors.invalid_vpatch')
        if not os.path.isfile(data['vpatch_path']):
            raise ValidationError, LANG.lookup('errors.vpatch_path')
      
      
        return data
    
    def save(self, data):
        # Language stuff
        if self.config.get('language') != data.get('language'):
            try:
                LANG.setLanguage(data['language'])
            except LanguageError, e:
                return UTL.show_error(LANG.lookup('errors.sorry'),
                                      LANG.lookup('errors.language'),
                                      wx.ICON_ERROR)
            else:
                self.local()

        self.config.update(data)
        
        self.config.save()
        return UTL.show_error(LANG.lookup('errors.success'),
                              LANG.lookup('errors.settings_updated'),
                              self.config,
                              wx.ICON_EXCLAMATION)
    
        
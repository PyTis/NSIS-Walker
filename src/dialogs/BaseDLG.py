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
#import sys

# Our Stuff
#import util as UTL
#import util.app as AP
#import util.configobj as COBJ
import util.images as IMG
#from util import my_button as BUTTONS
from util.language import language as LANG

# Third Party
import wx
import wx.lib.buttons  as  buttons

class BaseDLG(wx.Dialog, wx.Frame):
    label = None
    config = {} # loaded in init
    labels = []
    _buttons = []

    
    bg_bmp = None


    # Background for scrolled panel images.
    @property
    def default(self):
        return "#303030"
        
    # Program background color, by default
    @property
    def bgcolor(self):
        return None#"#303030"
        
    #Button Face Color
    @property
    def bt_bgcolor(self):
        return "#ffffff"
        
    #Button Text Color
    @property
    def bt_fgcolor(self):
        return "#0000a0"    
        
    # Font Text Color
    @property
    def fgcolor(self):
        return "#000000"
    
    @property
    def bg_image(self):
        return IMG.getProgramBitmap() 
    
    '''
    def _get_config(self):
        if not self._config:
            self._config = {}
        return self._config
    def _set_project(self, config):
        self._config = config
    config = property(_get_config, _set_config)
    '''

    def __init__(self, parent, 
                 id, 
                 title,
                 pos=(300,200),
                 size=(512,512),
                 style = wx.CAPTION
                        |wx.OK|wx.CANCEL
                        |wx.MINIMIZE_BOX 
                        |wx.CLOSE_BOX 
                        |wx.CLIP_CHILDREN
                       # |wx.TAB_TRAVERSAL
                        |wx.SYSTEM_MENU
                        ):
        self.labels = []              
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        
        self.config = wx.GetApp().config
        if not self.config.get('walker_options'):
            self.setDefaults()
            
        self.font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, )
        
        try:
            self.SetIcon(IMG.getWindowIcon())
        finally:
            pass
        self.setup()
        self.setColors() # handles skinning and language local
        #self.SetWindowShape()
    
    def setDefaults(self):
        self.config['walker_options'] = {
            '-D' : False,
            '-i' : True,
            '-F' : False,
            '-m0' : True,
            '-m1' : False,
            '-m2' : False,
        }
        self.config.save()
        
    ##################################################################
    # Setup
    def setup(self):
        pass
        


    def setCancelButton(self):
        self.cancel_button = buttons.GenButton(self, wx.ID_CANCEL, 'language',
                                    pos=(40,450),
                                    style=wx.BORDER_NONE&wx.BU_AUTODRAW)
          
        LANG.addButton(self.cancel_button, 'buttons.cancel', 'tooltips.cancel')
        self.Bind(wx.EVT_BUTTON, self.EndModal, self.cancel_button)
        self.colorBtn(self.cancel_button)

        
    ##################################################################
    # Wrappers


    #################################################################
    # Buttons Events.

    def EndModal(self, event):
        id = event.GetId()
        if id != wx.ID_OK and id != wx.ID_CANCEL:
            id = wx.ID_OK
        return wx.Dialog.EndModal(self, id)
    ##################################################################
    # Bakckground stuff.
    
        
    def SetWindowShape(self):
        #Use the bitmap's mask to determine the region
        r = wx.RegionFromBitmap(self.bg_bmp)
        self.hasShape = self.SetShape(r)
        
        
    
    def tileBackground(self, dc):
        # tile the background bitmap set by a property
        w = self.bg_bmp.GetWidth()
        h = self.bg_bmp.GetHeight()
        dc.DrawBitmap(self.bg_bmp, 0, 0)
        self.refreshLabels(dc)
        
    
    def onEraseBackground(self, evt):
        # Redraw the background over a 'damaged' area.
        if not self.bg_bmp:
            evt.Skip()
            return
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            dc.SetPalette(wx.NullPalette)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        self.tileBackground(dc)
    ##################################################################
    # Mechanics
    def local(self):
        LANG.local()
        self.Refresh()

    def colorBtn(self, btn):
        self._buttons.append(btn)
        if self.bt_fgcolor:
            btn.SetForegroundColour(self.bt_fgcolor)
        if self.bt_bgcolor:
            btn.SetBackgroundColour(self.bt_bgcolor)
            
            
            
    def colorBtns(self):
        for b in self._buttons:
            try:
                if self.bt_fgcolor:
                    b.SetForegroundColour(self.bt_fgcolor)
                if self.bt_bgcolor:
                    b.SetBackgroundColour(self.bt_bgcolor)
            except:
                pass
            
            
    def setColors(self):
        self.Unbind(wx.EVT_PAINT, self)
        self.bg_bmp = None
        if self.bgcolor:
            self.SetBackgroundColour(self.bgcolor)
        else:
            self.SetBackgroundColour(None)
        self.colorBtns()
        
        self.bg_bmp = self.bg_image
        if self.bg_bmp:
            mask = wx.Mask(self.bg_bmp)
            self.bg_bmp.SetMask(mask)
            self.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBackground)
        
        self.local()
        self.Refresh(True)


    def refreshLabels(self, dc=None):
        if not dc:
            dc = wx.ClientDC(self)
            dc.SetPalette(wx.NullPalette)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        for label in self.labels:
            if label:
                label.draw(dc)
                
    def StaticText(self, value, pos, event=None):
        """ These are not really static texts, to display text properly on a
            background image, I've decided to use a dc Cursor with a 
            custom mtext class.  To make the text's added the concept of 
            ranges, that are monitored by mouse movement.
            The words however can change in lenght with different language 
            packs, thus the mtext will control the range's size.
            
        """
        label = mtext(self, wx.NewId(), value, pos, event)
        self.labels.append(label)
        LANG.addStaticText(label, value)
        return label


# Custom Static text like class, uses a range from the parent to set events.
class mtext(object):
    _font = None
    _event = None
    _color = None
    _value = None
    width = 0
    height = 0
    id = None
    value = None
    
    def __init__(self, parent, id, value, pos, event=None):
        self._event = event
        self.parent = parent
        self.value = value
        pos = pos[0:2]
        self.pos = pos
        self.id = id
        
    def _get_font(self):
        if not self._font:
            self._font = self.parent.font
        return self._font
    def _set_font(self, font):
        self._font = font
    font = property(_get_font, _set_font)
    
    def SetFont(self, font):
        self.font=font
    
    def _get_fontcolor(self):
        if not self._color:
            self._color = self.parent.fgcolor
        return self._color
    def _set_fontcolor(self, color):
        self._color = color
    color = property(_get_fontcolor, _set_fontcolor)
    
    def _get_value(self):
        if not self._value:
            self._value = ''
        return self._value
    def _set_value(self, value):
        self._value = value
    value = property(_get_value, _set_value)
    
    def getSize(self):
        return (self.width, self.height)
    def setSize(self, s):
        self.width, self.height = s
        
    def draw(self, dc):
        #dc.SetPalette(wx.NullPalette)
        dc.SetFont(self.font)
        
        if self.color:    
            dc.SetTextForeground(self.color)
        x,y = self.pos
        tw, th = dc.GetTextExtent(self.value)
        dc.DrawText(self.value, x,y)
        self.setSize((tw,th))

    def GetId(self):
        return self.id
    
    def SetLabel(self, label):
        self.value = label
        
    



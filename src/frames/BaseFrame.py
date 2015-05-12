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
from util.language import language as LANG

# Third Party
import wx

class BaseFrame(wx.Frame):

    config = {} # loaded in init
    
    @property
    def fgcolor(self):
        return "#ffffff"
        
    @property
    def default(self):
        return "#3162a6"
        
    @property
    def bgcolor(self):
        return "#303030"
        
    @property
    def bt_bgcolor(self):
        return "#ffffff"
        
    @property
    def bt_fgcolor(self):
        return "#0000a0"
        
    @property
    def bg_image(self):
        return None
        
    
    def __init__(self, parent, title, pos=(400,400),
                  size=(350,192), style=wx.CAPTION
                                    |wx.MINIMIZE_BOX 
                                    |wx.CLOSE_BOX 
                                    |wx.CLIP_CHILDREN
                                    |wx.TAB_TRAVERSAL
                                    |wx.SYSTEM_MENU
                                     ):
        
        self.parent = parent
        self.debug = wx.GetApp().debug
        self.config = wx.GetApp().config
        
        if not title:
            title = ''
        
        wx.Frame.__init__(self, parent=parent, title=title,
                          pos=pos, size=size, style=style)
        self.skin()
        self.setup()
        
        #self.SetWindowShape() # sytle = wx.FRAME_SHAPED
            
    def setup(self):
        pass
    
        
    def local(self):
        return LANG.local()
    
    def skin(self):
        self.Unbind(wx.EVT_PAINT, self)
        self.bg_bmp = None
        if self.bgcolor:
            self.SetBackgroundColour(self.bgcolor)
        else:
            self.SetBackgroundColour(None)
          
        if self.bg_image:
            self.bg_bmp = self.bg_image
            mask = wx.Mask(self.bg_bmp)
            self.bg_bmp.SetMask(mask)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBackground)
        self.CenterOnScreen()
        self.Refresh(True)

        
    ##################################################################
    # Bakckground stuff.
    # tile the background bitmap set by a property
    def tileBackground(self, dc):
        if self.bg_image:
            w = self.bg_bmp.GetWidth()
            h = self.bg_bmp.GetHeight()
            dc.DrawBitmap(self.bg_bmp, 0, 0)
        
    # Redraw the background over a 'damaged' area.
    def onEraseBackground(self, evt):
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

        
    def SetWindowShape(self):
        #Use the bitmap's mask to determine the region
        
        r = wx.RegionFromBitmap(self.bg_bmp)
        self.hasShape = self.SetShape(r)
        
    
    def OnClose(self, e):
      
        return self.onCloseFrame(e)
    
    def onCloseFrame(self, e):
        try:
            self.onCloseApp(e)
        except TypeError, e:
            self.Destroy()
    
    def onCloseApp(self, e):
        return self.Close()
        self.parent.exit()
        wx.GetApp().exit()
        
                    
    
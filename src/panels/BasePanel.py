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
# Built in

# Our stuff
import util as UTL
from util.language import language as LANG

# 3rd Party
import wx


class BasePanel(wx.Panel): 

    config = {} # loaded in init
    _ranges = [] # cursor ranges
    _cur_range = None # Current cursor range
    labels = []
    _buttons = []
    bg_bmp = None
    # Font Text Color
    @property
    def fgcolor(self):
        return "#00187A"
        
    # Background for scrolled panel images.
    @property
    def default(self):
        return "#303030"
        
    # Program background color, by default
    @property
    def bgcolor(self):
        return "#303030"
        
    #Button Face Color
    @property
    def bt_bgcolor(self):
        return "#ffffff"
        
    #Button Text Color
    @property
    def bt_fgcolor(self):
        return "#0000a0"
        
    @property
    def bg_image(self):
        return None

    def onShowSettings(self,e):
        self.parent.showSettings()
    def onShowPrograms(self,e):
        self.parent.showPrograms()
   
        
    def __init__(self, parent, pos=wx.DefaultPosition, size=(698,592)):
        wx.Panel.__init__(self, parent, -1, pos, size, 
                          style=wx.DEFAULT|wx.TAB_TRAVERSAL)
        self.labels = []
        self._buttons = []
        
        self.parent = parent
       
        self.debug = parent.debug
        self.config = wx.GetApp().config

        self.font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, )
                
        self.setup()
        self.setColors() # handles skinning and language local
        
        self.Bind(wx.EVT_MOTION, self.rangeOver, self)
        self.Bind(wx.EVT_LEFT_UP, self.rangeUp, self)
        self.Bind(wx.EVT_LEFT_DOWN, self.rangeDown, self)
        self.postLoad()
        
    def postLoad(self):
        pass
    ###########################################################################
    # Range Mouse capturing for labels to function like buttons.
    def addRange(self, min_x, min_y, width, height, event):
        self._ranges.append(((min_x, min_y, min_x+width, min_y+height),
                            event))
          
    def clearRanges(self):
        self._ranges = []

    def SetWindowShape(self):
        #Use the bitmap's mask to determine the region
        r = wx.RegionFromBitmap(self.bg_bmp)
        self.hasShape = self.SetShape(r)
        
        
    def rangeOver(self, e):
        x,y = e.GetPosition()

        for range in self._ranges:
            min_x, min_y, max_x, max_y = range[0]
            if x > min_x and x < max_x and y > min_y and y < max_y:
                self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
                return True
        else:
            self.SetCursor(wx.NullCursor)
            return True
     
    def rangeDown(self, e):
        self._cur_range = None
        x,y = e.GetPosition()

        for range in self._ranges:
            min_x, min_y, max_x, max_y = range[0]
            if x > min_x and x < max_x and y > min_y and y < max_y:
                self._cur_range = range[1].__name__
                
                
    def rangeUp(self, e):
        current = self._cur_range
        self._cur_range = None
        x,y = e.GetPosition()
        for range in self._ranges:
            min_x, min_y, max_x, max_y = range[0]
            if x > min_x and x < max_x and y > min_y and y < max_y:
                if current == range[1].__name__:
                    return range[1](e)
            

    ###########################################################################
    # overridable methods
    def setup(self):
        """
        To make our init less complicated this calls the methods that draw
        the default background stuff on our panes.  This can be overridden
        in the future to not show some of the features below
        """
        pass

    ##################################################################
    # Buttons Events / Actions

    
    def onMinimize(self, e):
        wx.GetApp().Minimize(None)
        return True

    def onCloseFrame(self, e):
        try:
            self.parent.onCloseFrame(e)
        except TypeError, e:
            self.parent.Destroy()
    
    def onCloseApp(self, e):
        wx.GetApp().exit()
        
        
    def showFrame(self, frame, tooltip):
        def _(e):
            wx.GetApp().loadFrame(self, frame, tooltip)
        return _


    def browseAction(self, path): return wx.GetApp().browseAction(path)

    def makeRun(self, path): return wx.GetApp().makeRun(path)

    def makeChildProgram(self, path): return wx.GetApp().makeChildProgram(path)

    
    def futureFeature(self, evt):
        return UTL.show_error(LANG.lookup('errors.comming_soon'),
                       LANG.lookup('errors.not_implemented'),
                       self.config,
                       wx.ICON_INFORMATION)
   

   
    ##################################################################
    # Lanaguage and skinning
    
    
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
        self.clearRanges()
        for label in self.labels:
            if label:
                label.draw(dc)
                label.setupEventRange()
                
    ##################################################################
    # Bakckground stuff.
    # tile the background bitmap set by a property
    def tileBackground(self, dc):
        w = self.bg_bmp.GetWidth()
        h = self.bg_bmp.GetHeight()
        dc.DrawBitmap(self.bg_bmp, 0, 0)
        self.refreshLabels(dc)
        
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

    def onRefreshLabels(self, evt):
        dc = wx.PaintDC(self)
        self.refreshLabels(dc)
        evt.Skip()


    ##################################################################

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
    pos = (0,0)
    
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
    
    def setupEventRange(self):
        if self._event:
            min_x, min_y = self.pos
            width, height = self.getSize()
            self.parent.addRange(min_x, min_y, width, height, self._event)

    def GetId(self):
        return self.id
    
    def SetLabel(self, label):
        self.value = label
    
    def SetPosition(self, p):
        self.pos = p
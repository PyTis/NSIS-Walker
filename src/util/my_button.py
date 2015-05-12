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

# 3rd Party
import wx
from wx import BitmapButton
from wx.lib.buttons import GenBitmapTextButton

__all__ = ['PicButton', 'PicTextButton']

class _WinFlatPicTextMixin:
    """
    Emulates a win32 flat button
    Default-state:border=0
    hover:border=1
    down:do not change colour
    """
    fsize_w = 0
    fsize_h = 0
    def __init__(self):
        self.useFocusInd = False
        self.bezelWidth = 0
        self.Bind(wx.EVT_ENTER_WINDOW ,self.OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW ,self.OnMouseLeave)
        self.fsize_w, self.fsize_h = self.GetSize()
        
    def OnMouseEnter(self,event):
        self.bezelWidth = 1
        self.Refresh()
        
    def OnMouseLeave(self,event):
        self.bezelWidth = 0
        self.Refresh()
        
    def OnPaint(self, event):
        """
        copy&paste from GenButton with 1 minor change(colour on down)
        """
        (width, height) = self.GetClientSizeTuple()
        x1 = y1 = 0
        x2 = width-1
        y2 = height-1
        dc = wx.BufferedPaintDC(self)
        brush = None
        self.SetSize((self.fsize_w,self.fsize_h))

        colBg = self.GetBackgroundColour()
        brush = wx.Brush(colBg, wx.SOLID)
        if self.style & wx.BORDER_NONE:
            myAttr = self.GetDefaultAttributes()
            parAttr = self.GetParent().GetDefaultAttributes()
            myDef = colBg == myAttr.colBg
            parDef = self.GetParent().GetBackgroundColour() == parAttr.colBg
            if myDef and parDef:
                if wx.Platform == "__WXMAC__":
                    brush.MacSetTheme(1) # 1 == kThemeBrushDialogBackgroundActive
                elif wx.Platform == "__WXMSW__":
                    if self.DoEraseBackground(dc):
                        brush = None
            elif myDef and not parDef:
                colBg = self.GetParent().GetBackgroundColour()
                brush = wx.Brush(colBg, wx.SOLID)


        if brush is not None:
            dc.SetBackground(brush)
            dc.Clear()
        self.DrawBezel(dc, x1, y1, x2, y2)
        self.DrawLabel(dc, width, height)
        if self.hasFocus and self.useFocusInd:
            self.DrawFocusIndicator(dc, width, height)
            
    def DrawLabel(self, dc, width, height, dw=0, dy=0):
        bmp = self.bmpLabel
        if bmp != None:     # if the bitmap is used
            if self.bmpDisabled and not self.IsEnabled():
                bmp = self.bmpDisabled
            if self.bmpFocus and self.hasFocus:
                bmp = self.bmpFocus
            if self.bmpSelected and not self.up:
                bmp = self.bmpSelected
            bw,bh = bmp.GetWidth(), bmp.GetHeight()
            if not self.up:
                dw = dy = self.labelDelta
            hasMask = bmp.GetMask() != None
        else:
            bw = bh = 0     # no bitmap -> size is zero

        dc.SetFont(self.GetFont())
        if self.IsEnabled():
            dc.SetTextForeground(self.GetForegroundColour())
        else:
            dc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))

        label = self.GetLabel()
        tw, th = dc.GetTextExtent(label)        # size of text
        if not self.up:
            dw = dy = self.labelDelta

        #pos_x = (width-bw-tw)/2+dw      # adjust for bitmap and text to centre
        pos_x = 6 # not centered, but left aligned
        if bmp !=None:
            dc.DrawBitmap(bmp, pos_x, (height-bh)/2+dy, hasMask) # draw bitmap if available
            pos_x = pos_x + 2   # extra spacing from bitmap

        dc.DrawText(label, pos_x+4 + dw+bw, (height-th)/2+dy)      # draw the text


class _WinFlatPicMixin:
    """
    Emulates a win32 flat button
    Default-state:border=0
    hover:border=1
    down:do not change colour
    """
    fsize_w = 0
    fsize_h = 0
    def __init__(self):
        self.useFocusInd = False
        self.bezelWidth = 0
        self.Bind(wx.EVT_ENTER_WINDOW ,self.OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW ,self.OnMouseLeave)
        #self.Bind(wx.EVT_LEFT_DOWN ,self.OnMouseDown)
        self.fsize_w, self.fsize_h = self.GetSize()
        
        
    def OnMouseEnter(self,event):
        self.bezelWidth = 0
        self.Refresh()
    def OnMouseLeave(self,event):
        self.bezelWidth = 0
        self.Refresh()
        
    def OnMouseDown(self, event):
        self.bezelWidth = 0
        self.Refresh()
        
    def DrawBezel(self, dc, x1, y1, x2, y2):
        """ Use this to draw our own 
        """
        return 
    
    def OnPaint(self, event):
        """
        copy&paste from GenButton with 1 minor change(colour on down)
        """
        (width, height) = self.GetClientSizeTuple()
        x1 = y1 = 0
        x2 = width-1
        y2 = height-1

            
        dc = wx.BufferedPaintDC(self)
        brush = None
        self.SetSize((self.fsize_w,self.fsize_h))
        colBg = self.GetBackgroundColour()
        brush = wx.Brush(colBg, wx.SOLID)
        if self.style & wx.BORDER_NONE:
            myAttr = self.GetDefaultAttributes()
            parAttr = self.GetParent().GetDefaultAttributes()
            myDef = colBg == myAttr.colBg
            parDef = self.GetParent().GetBackgroundColour() == parAttr.colBg
            if myDef and parDef:
                if wx.Platform == "__WXMAC__":
                    brush.MacSetTheme(1) # 1 == kThemeBrushDialogBackgroundActive
                elif wx.Platform == "__WXMSW__":
                    if self.DoEraseBackground(dc):
                        brush = None
            elif myDef and not parDef:
                colBg = self.GetParent().GetBackgroundColour()
                brush = wx.Brush(colBg, wx.SOLID)
        if brush is not None:
            dc.SetBackground(brush)
            dc.Clear()
        self.DrawLabel(dc, width, height)
        if self.hasFocus and self.useFocusInd:
            self.DrawFocusIndicator(dc, width, height)

    def DrawLabel(self, dc, width, height, dw=0, dy=0):
        bmp = self.bmpLabel
        if bmp != None:     # if the bitmap is used
            if self.bmpDisabled and not self.IsEnabled():
                bmp = self.bmpDisabled
            if self.bmpFocus and self.hasFocus:
                bmp = self.bmpFocus
            if self.bmpSelected and not self.up:
                bmp = self.bmpSelected
            bw,bh = bmp.GetWidth(), bmp.GetHeight()
            if not self.up:
                dw = dy = self.labelDelta
            hasMask = bmp.GetMask() != None
        if bmp !=None:
            dc.DrawBitmap(bmp, -1, -1, bmp.GetMask() != None) # draw bitmap if available
 


class PicButton(_WinFlatPicMixin,BitmapButton):
    def __init__(self,*arg,**kwarg):
        BitmapButton.__init__(self,*arg,**kwarg)
        _WinFlatPicMixin.__init__(self)

class PicTextButton(_WinFlatPicTextMixin,GenBitmapTextButton):
    def __init__(self,*arg,**kwarg):
        GenBitmapTextButton.__init__(self,*arg,**kwarg)
        _WinFlatPicTextMixin.__init__(self)
        
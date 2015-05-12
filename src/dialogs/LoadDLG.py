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
import util as UTL
from util.language import language as LANG

# Third Party
import wx


class LoadDLG(wx.Dialog):
    currentItem = None
    name = None
    config = {}
    parent = None
    
    def __init__(self,parent,id,title,name,options,config,
                 style = wx.CAPTION
                    |wx.OK|wx.CANCEL
                    |wx.CLIP_CHILDREN
                   #|wx.TAB_TRAVERSAL
                    ):
        
        wx.Dialog.__init__(self, 
                           parent=parent, 
                           id=id,
              
                           title=LANG.lookup(title),
                           style=style,
                           size=(400,350),
                           name=LANG.lookup(name))
        self.config = config
        self.parent = parent
        self.lc = wx.ListCtrl(self, -1,
                               pos=(20,10), size=(350,250),
                                 style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        self.lc.InsertColumn(0, 'State')
        self.lc.InsertColumn(1, 'Capital')
        self.lc.SetColumnWidth(0, 175)
        self.lc.SetColumnWidth(1, 171)
        self.options = options
        self.setItems()

        cnbttn = wx.Button(self, wx.ID_CANCEL, LANG.lookup('load.buttons.cancel'),(20, 285))
        
        okbttn = wx.Button(self, -1, LANG.lookup('buttons.ok'), (298, 285))
        self.Bind(wx.EVT_BUTTON, self.EndModal, okbttn)
        
        remove = wx.Button(self, -1, LANG.lookup('buttons.remove'),(150, 285))
        
        self.Bind(wx.EVT_BUTTON, self.onRemove, remove)
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.lc)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.lc)

        self.lc.Bind(wx.EVT_LEFT_DCLICK, self.EndModal)
        
    def setItems(self):
        for o in self.options:
            num_items = self.lc.GetItemCount()
            self.lc.InsertStringItem(num_items, o[0])
            self.lc.SetStringItem(num_items, 1, o[1])

    def EndModal(self, event):
        id = event.GetId()
        if id != wx.ID_OK and id != wx.ID_CANCEL: # double clicked
            id = wx.ID_OK
        if id == wx.ID_OK and not self.name:
            UTL.show_error(LANG.lookup('load.errors.nofile'),
                           LANG.lookup('load.errors.nofile_long'),
                           self.config)
            event.Skip()
            return
        elif id == wx.ID_OK:
            self.parent.load(self.name)
            
        return wx.Dialog.EndModal(self, id)
    
    def onRemove(self, event):
        dlg = wx.MessageDialog(self,
                               LANG.lookup('load.check_remove'),
                               LANG.lookup('load.check'),
                               wx.YES_NO
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        if dlg.ShowModal() == wx.ID_YES:
            self.remove()
        dlg.Destroy()
        
    def remove(self):
        if self.name:
            self.lc.DeleteAllItems()
            del self.parent.config['projects'][self.name]
            self.parent.config.save()
            self.options = self.parent.getOptions()
            self.setItems()
            self.name=None
            
    
    def getColumnText(self, index, col):
        item = self.lc.GetItem(index, col)
        return item.GetText()

    def OnItemSelected(self, event):
        self.name = self.getColumnText(event.m_itemIndex, 0)
        event.Skip()

    def OnItemDeselected(self, evt):
        self.name = None 
        








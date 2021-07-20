#!/usr/bin/env python

import wx


class ViewMenu(wx.Menu):

    def __init__(self, parent):
        super(ViewMenu, self).__init__()
        self.parent = parent

        self.show_status = self.Append(wx.ID_ANY, 'Show statusbar',
                                       'Show Statusbar', kind=wx.ITEM_CHECK)
        self.show_toolbar = self.Append(wx.ID_ANY, 'Show toolbar',
                                        'Show Toolbar', kind=wx.ITEM_CHECK)
        self.Check(self.show_status.GetId(), True)
        self.Check(self.show_toolbar.GetId(), True)
        self.Bind(wx.EVT_MENU, self.toggle_status_bar, self.show_status)
        self.Bind(wx.EVT_MENU, self.toggle_tool_bar, self.show_toolbar)

    def toggle_status_bar(self, e):
        if self.show_status.IsChecked():
            self.parent.statusbar.Show()
        else:
            self.parent.statusbar.Hide()

    def toggle_tool_bar(self, e):
        if self.show_toolbar.IsChecked():
            self.parent.toolbar.Show()
        else:
            self.parent.toolbar.Hide()

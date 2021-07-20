#!/usr/bin/env python

import wx


class ContextMenu(wx.Menu):

    def __init__(self, parent):
        super(ContextMenu, self).__init__()
        self.parent = parent

        minimize = wx.MenuItem(self, wx.NewId(), 'Minimize')
        self.Append(minimize)
        self.Bind(wx.EVT_MENU, self.on_minimize, minimize)

        close = wx.MenuItem(self, wx.NewId(), 'Close')
        self.Append(close)
        self.Bind(wx.EVT_MENU, self.on_close, close)

    def on_close(self, e):
        self.parent.Close()

    def on_minimize(self, e):
        self.parent.Iconize()

#!/usr/bin/env python

import os
import wx
from wxGui.chaimGui.about import About

APP_EXIT = 1
DIR = os.path.dirname(__file__)


class FileMenu(wx.Menu):

    def __init__(self, parent):
        super(FileMenu, self).__init__()
        self.parent = parent

        self.Append(wx.ID_NEW, '&New')
        self.Append(wx.ID_OPEN, '&Open')
        self.Append(wx.ID_SAVE, '&Save')
        self.AppendSeparator()
        imp = wx.Menu()
        imp.Append(wx.ID_ANY, 'Import newsfeed list...')
        imp.Append(wx.ID_ANY, 'Import bookmarks...')
        imp.Append(wx.ID_ANY, 'Import mail...')
        self.Append(wx.ID_ANY, '&Import', imp)
        self.AppendSeparator()

        file_item_about = self.Append(wx.ID_ABOUT, '&About', 'About application')
        self.Bind(wx.EVT_MENU, self.on_about, file_item_about)

        qmi = wx.MenuItem(self, APP_EXIT, '&Quit\tCtrl+Q')
        qmi.SetBitmap(wx.Bitmap(os.path.join(DIR, 'icons/exit.png')))
        self.Append(qmi)
        self.Bind(wx.EVT_MENU, self.on_quite, id=APP_EXIT)

    def on_quite(self, e):
        self.parent.Close()

    def on_about(self, e):
        About()



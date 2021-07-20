#!/usr/bin/env python

import os
import wx
from wxGui.chaimGui.file_menu import FileMenu
from wxGui.chaimGui.view_menu import ViewMenu
from wxGui.chaimGui.context_menu import ContextMenu
from wxGui.chaimGui.dialog import Dialog
from wxGui.chaimGui.rename_dialog import RenameDialog
from wxGui.chaimGui.content import Content

DIR = os.path.dirname(__file__)


class MainWindow(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.statusbar = self.CreateStatusBar()
        self.toolbar = self.CreateToolBar()
        self.init_ui()

    def init_ui(self):
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)

        menu_bar = wx.MenuBar()
        file_menu = FileMenu(self)
        view_menu = ViewMenu(self)
        self.SetMenuBar(menu_bar)
        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(view_menu, '&View')

        qtool = self.toolbar.AddTool(wx.ID_ANY, 'Quit', wx.Bitmap(os.path.join(DIR, 'icons/exit.png')))
        self.toolbar.Realize()
        self.Bind(wx.EVT_TOOL, self.on_dialog, qtool)

        self.statusbar.SetStatusText('Ready')

        self.SetSize(600, 450)
        self.Center()
        self.SetTitle("Barcode Recognizer")
        self.SetLayoutDirection(wx.Layout_LeftToRight)
        self.SetWindowStyle(wx.MAXIMIZE_BOX | wx.RESIZE_BORDER
                            | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
                            | wx.MINIMIZE_BOX)

        Content(self)

    def on_quit(self, e):
        self.Close()

    def on_right_down(self, e):
        self.PopupMenu(ContextMenu(self), e.GetPosition())

    def on_dialog(self, e):
        dialog = RenameDialog(None)
        dialog.SetLayoutDirection(wx.Layout_LeftToRight)
        dialog.Show()



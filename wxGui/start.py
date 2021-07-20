#!/usr/bin/env python
"""
PDF Barcode recognition app
"""
import wx
from wxGui.chaimGui.main_window import MainWindow


def main():
    app = wx.App()
    gui = MainWindow(None)
    gui.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()

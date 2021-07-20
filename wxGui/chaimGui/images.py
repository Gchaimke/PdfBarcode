#!/usr/bin/env python

import wx
import os

DIR = os.path.dirname(__file__)


class Images(wx.Panel):

    def __init__(self, parent):
        super(Images, self).__init__()
        self.parent = parent
        self.load_images()

        self.mincol.SetPosition((20, 20))
        self.bardejov.SetPosition((40, 160))
        self.rotunda.SetPosition((170, 50))

    def load_images(self):
        self.mincol = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                      wx.Bitmap(os.path.join(DIR, '../images/avr-100-c.png'), wx.BITMAP_TYPE_ANY))

        self.bardejov = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                        wx.Bitmap(os.path.join(DIR, '../images/printer.jpg'), wx.BITMAP_TYPE_ANY))

        self.rotunda = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                       wx.Bitmap(os.path.join(DIR, '../images/tal.png'), wx.BITMAP_TYPE_ANY))
# -*- coding: UTF-8 -*-

import wx
from MainFrame import MainFrame


class PdfBarcode(wx.App):
    def OnInit(self):
        self.main_frame = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.main_frame)
        self.main_frame.Show()
        return True
# end of class PdfBarcode


if __name__ == "__main__":
    app = PdfBarcode(0)
    app.MainLoop()

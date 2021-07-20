#!/usr/bin/env python

import wx
import wx.adv


class About(wx.adv.AboutDialogInfo):

    def __init__(self, *args, **kwargs):
        super(About, self).__init__(*args, **kwargs)

        description = """File Hunter is an advanced file manager for
the Unix operating system. Features include powerful built-in editor,
advanced search capabilities, powerful batch renaming, file comparison,
extensive archive handling and more.
"""

        licence = """File Hunter is free software; you can redistribute
it and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.

File Hunter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details. You should have
received a copy of the GNU General Public License along with File Hunter;
if not, write to the Free Software Foundation, Inc., 59 Temple Place,
Suite 330, Boston, MA  02111-1307  USA"""

        #self.SetIcon(wx.Icon('hunter.png', wx.BITMAP_TYPE_PNG))
        self.SetName('File Hunter')
        self.SetVersion('1.0')
        self.SetDescription(description)
        self.SetCopyright('(C) 2007 - 2021 Jan Bodnar')
        self.SetWebSite('http://www.zetcode.com')
        self.SetLicence(licence)
        self.AddDeveloper('Jan Bodnar')
        self.AddDocWriter('Jan Bodnar')
        self.AddArtist('The Tango crew')
        self.AddTranslator('Jan Bodnar')
        wx.adv.AboutBox(self)

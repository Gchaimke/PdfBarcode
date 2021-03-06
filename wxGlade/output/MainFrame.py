# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.2 on Thu Jul 15 10:27:53 2021
#

import wx
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MainFrame(wx.Frame):
	def __init__(self, *args, **kwds):
		# begin wxGlade: MainFrame.__init__
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
		wx.Frame.__init__(self, *args, **kwds)
		self.SetTitle(_("PdfBarcode"))
		_icon = wx.NullIcon
		_icon.CopyFromBitmap(wx.Bitmap("icons/PdfBarcode.png", wx.BITMAP_TYPE_ANY))
		self.SetIcon(_icon)

		# Menu Bar
		self.menubar = wx.MenuBar()
		wxglade_tmp_menu = wx.Menu()
		self.menubar.Append(wxglade_tmp_menu, _("File"))
		self.SetMenuBar(self.menubar)
		# Menu Bar end

		sizer_1 = wx.GridBagSizer(0, 0)

		self.spliter_window = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_3DBORDER | wx.SP_LIVE_UPDATE | wx.SP_PERMIT_UNSPLIT)
		self.spliter_window.SetMinimumPaneSize(400)
		self.spliter_window.SetSashGravity(0.5)
		sizer_1.Add(self.spliter_window, (0, 0), (1, 1), wx.EXPAND, 0)

		self.previw_pane = wx.ScrolledWindow(self.spliter_window, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
		self.previw_pane.SetScrollRate(10, 10)

		hbox_preview = wx.FlexGridSizer(1, 1, 0, 0)

		image_preview = wx.StaticBitmap(self.previw_pane, wx.ID_ANY, wx.Bitmap("tmp/tmp0001.png", wx.BITMAP_TYPE_ANY))
		hbox_preview.Add(image_preview, 0, wx.ALL | wx.EXPAND, 10)

		self.recognation_pane = wx.Panel(self.spliter_window, wx.ID_ANY)

		vbox_recognition = wx.BoxSizer(wx.VERTICAL)

		vbox_start = wx.BoxSizer(wx.VERTICAL)
		vbox_recognition.Add(vbox_start, 0, wx.EXPAND, 0)

		self.start_btn = wx.Button(self.recognation_pane, wx.ID_ANY, _("Start Recognition"))
		self.start_btn.SetMinSize((195, 40))
		self.start_btn.SetBackgroundColour(wx.Colour(132, 203, 255))
		self.start_btn.SetForegroundColour(wx.Colour(0, 0, 0))
		self.start_btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
		self.start_btn.SetFocus()
		vbox_start.Add(self.start_btn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

		self.progress_gauge = wx.Gauge(self.recognation_pane, wx.ID_ANY, 100, style=0)
		vbox_start.Add(self.progress_gauge, 0, wx.ALL | wx.EXPAND, 5)

		hbox_lists = wx.BoxSizer(wx.HORIZONTAL)
		vbox_recognition.Add(hbox_lists, 1, wx.ALL | wx.EXPAND, 5)

		self.list_not_recognized = wx.ListCtrl(self.recognation_pane, wx.ID_ANY, style=wx.FULL_REPAINT_ON_RESIZE | wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
		self.list_not_recognized.SetBackgroundColour(wx.Colour(255, 201, 205))
		self.list_not_recognized.AppendColumn(_("Not Recognized"), format=wx.LIST_FORMAT_LEFT, width=200)
		self.list_not_recognized.AppendColumn("", format=wx.LIST_FORMAT_LEFT, width=0)
		self.list_not_recognized.AppendColumn("", format=wx.LIST_FORMAT_LEFT, width=0)
		hbox_lists.Add(self.list_not_recognized, 1, wx.ALL | wx.EXPAND, 5)

		self.list_recognized = wx.ListCtrl(self.recognation_pane, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
		self.list_recognized.SetBackgroundColour(wx.Colour(196, 255, 216))
		self.list_recognized.AppendColumn(_("Recognized"), format=wx.LIST_FORMAT_LEFT, width=200)
		self.list_recognized.AppendColumn("", format=wx.LIST_FORMAT_LEFT, width=0)
		self.list_recognized.AppendColumn("", format=wx.LIST_FORMAT_LEFT, width=0)
		hbox_lists.Add(self.list_recognized, 1, wx.ALL | wx.EXPAND, 5)

		self.list_selection = wx.ListCtrl(self.recognation_pane, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_ICON | wx.LC_VRULES)
		vbox_recognition.Add(self.list_selection, 1, wx.ALL | wx.EXPAND, 10)

		hbox_save = wx.BoxSizer(wx.HORIZONTAL)
		vbox_recognition.Add(hbox_save, 0, wx.ALL | wx.EXPAND, 10)

		self.txt_name = wx.TextCtrl(self.recognation_pane, wx.ID_ANY, "")
		hbox_save.Add(self.txt_name, 3, wx.ALIGN_BOTTOM | wx.ALL, 5)

		self.save_btn = wx.Button(self.recognation_pane, wx.ID_ANY, _("Save"))
		self.save_btn.SetBackgroundColour(wx.Colour(70, 212, 110))
		self.save_btn.SetForegroundColour(wx.Colour(9, 40, 88))
		self.save_btn.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
		hbox_save.Add(self.save_btn, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)

		self.recognation_pane.SetSizer(vbox_recognition)

		hbox_preview.AddGrowableRow(0)
		hbox_preview.AddGrowableCol(0)
		self.previw_pane.SetSizer(hbox_preview)

		self.spliter_window.SplitVertically(self.previw_pane, self.recognation_pane)

		sizer_1.AddGrowableRow(0)
		sizer_1.AddGrowableCol(0)
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)
		sizer_1.SetSizeHints(self)

		self.Layout()
		self.Centre()
		# end wxGlade

# end of class MainFrame

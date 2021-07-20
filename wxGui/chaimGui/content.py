#!/usr/bin/env python

import wx

TASK_RANGE = 50


class Content(wx.Panel):

    def __init__(self, parent):
        super(Content, self).__init__()
        self.parent = parent

        panel = wx.Panel(parent)
        rec_box = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        start_box = wx.BoxSizer(wx.VERTICAL)
        btn_start = wx.Button(panel, wx.ID_ANY, 'Start')
        gauge = wx.Gauge(panel, range=TASK_RANGE, size=(250, -1))
        start_box.Add(btn_start, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        start_box.Add(gauge, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        hbox1.Add(start_box, proportion=1, flag=wx.ALIGN_CENTRE_VERTICAL)

        list_box = wx.BoxSizer(wx.HORIZONTAL)
        listbox1 = wx.ListBox(panel, id=wx.ID_ANY)
        listbox2 = wx.ListBox(panel, id=wx.ID_ANY)
        list_box.Add(listbox1, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        list_box.Add(listbox2,  proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        start_box.Add(list_box, 1, wx.EXPAND | wx.LEFT, 20)

        btnPanel = wx.Panel(panel)
        vbox = wx.BoxSizer(wx.VERTICAL)

        listbox3 = wx.ListBox(btnPanel, id=wx.ID_ANY)
        renBtn = wx.Button(btnPanel, wx.ID_ANY, 'Rename', size=(90, 30))

        vbox.Add(listbox3, wx.ID_ANY, wx.EXPAND | wx.ALL, 10)
        vbox.Add((-1, 20))
        vbox.Add(renBtn, 0, wx.TOP, 5)

        btnPanel.SetSizer(vbox)
        hbox2.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
        panel.SetSizerAndFit(hbox2)

        self.Bind(wx.EVT_BUTTON, self.NewItem, id=btn_start.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnRename, id=renBtn.GetId())
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnRename)

    def NewItem(self, event):

        text = wx.GetTextFromUser('Enter a new item', 'Insert dialog')
        if text != '':
            self.listbox.Append(text)

    def OnRename(self, event):

        sel = self.listbox.GetSelection()
        text = self.listbox.GetString(sel)
        renamed = wx.GetTextFromUser('Rename item', 'Rename dialog', text)

        if renamed != '':
            self.listbox.Delete(sel)
            item_id = self.listbox.Insert(renamed, sel)
            self.listbox.SetSelection(item_id)

    def OnDelete(self, event):

        sel = self.listbox.GetSelection()
        if sel != -1:
            self.listbox.Delete(sel)

    def OnClear(self, event):
        self.listbox.Clear()



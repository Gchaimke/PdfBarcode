# -*- coding: UTF-8 -*-
import fitz
import gettext
import wx
from pyzbar import pyzbar
from pdf2image import convert_from_path
from os.path import join
from shutil import move, copyfile
import tempfile
import cv2
import re
from datetime import datetime
from pathlib import Path
import configparser
import threading

config = configparser.ConfigParser()

conf_file = Path('config.ini')
if conf_file.exists():
	config.read('config.ini')
else:
	config.add_section("default")
	config.set("default", "input_folder", "pdf")
	config.set("default", "output_folder", "pdf\\output")
	config.set("default", "regex", "^0[3,0][0,6,9]\\d+$")
	config.set("default", "wait", 'False')
	config.set("default", "poppler_path", 'poppler_21_03_0')
	config.set("default", "tumb_folder", '~\\Pictures')
	config.set("default", "language", 'he')
	config_file = open("config.ini", 'w')
	config.write(config_file)
	config_file.close()
	config.read('config.ini')

config = config['default']

poppler_path = config.get('poppler_path')

# end wxGlade


class MainFrame(wx.Frame):
	def __init__(self, *args, **kwds):
		# begin wxGlade: MainFrame.__init__
		
		he = gettext.translation('pdf_barcode', localedir='locale', languages=[config.get('language')])
		he.install()
		
		self.preview_image_size = (400, 500)
		self.preview_image_path = ""
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
		wx.Frame.__init__(self, *args, **kwds)
		self.SetTitle(_("PdfBarcode"))
		_icon = wx.NullIcon
		_icon.CopyFromBitmap(wx.Bitmap("icons\PdfBarcode.png", wx.BITMAP_TYPE_ANY))
		self.SetIcon(_icon)
		
		# Menu Bar
		self.menubar = wx.MenuBar()
		wxglade_tmp_menu = wx.Menu()
		self.menubar.Append(wxglade_tmp_menu, _("File"))
		self.SetMenuBar(self.menubar)
		# Menu Bar end
		
		self.sizer_1 = wx.GridBagSizer(1, 1)
		self.sizer_1.SetMinSize(700, 600)
		
		self.splitter_window = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_3DBORDER | wx.SP_LIVE_UPDATE | wx.SP_PERMIT_UNSPLIT)
		self.splitter_window.SetMinimumPaneSize(400)
		self.splitter_window.SetSashGravity(0.5)
		self.sizer_1.Add(self.splitter_window, (0, 0), (1, 1), wx.EXPAND, 0)
		
		self.preview_pane = wx.ScrolledWindow(self.splitter_window, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
		self.preview_pane.SetScrollRate(10, 10)
		self.preview_pane.SetSize((400, 800))
		hbox_preview = wx.FlexGridSizer(1, 1, 0, 0)
		
		self.bmp = wx.Bitmap(self.preview_image_size, 2)
		self.image_preview = wx.StaticBitmap(self.preview_pane, wx.ID_ANY, wx.Bitmap(self.bmp))
		hbox_preview.Add(self.image_preview, 0, wx.ALL | wx.EXPAND, 10)
		
		self.recognition_pane = wx.Panel(self.splitter_window, wx.ID_ANY)
		
		vbox_recognition = wx.BoxSizer(wx.VERTICAL)
		
		vbox_start = wx.BoxSizer(wx.VERTICAL)
		vbox_recognition.Add(vbox_start, 0, wx.EXPAND, 0)
		
		self.start_btn = wx.Button(self.recognition_pane, wx.ID_ANY, _("Start Recognition"))
		self.start_btn.SetMinSize((195, 40))
		self.start_btn.SetBackgroundColour(wx.Colour(132, 203, 255))
		self.start_btn.SetForegroundColour(wx.Colour(0, 0, 0))
		self.start_btn.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
		self.start_btn.SetFocus()
		vbox_start.Add(self.start_btn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
		
		self.progress_gauge = wx.Gauge(self.recognition_pane, wx.ID_ANY, 100, style=0)
		vbox_start.Add(self.progress_gauge, 0, wx.ALL | wx.EXPAND, 5)
		
		hbox_lists = wx.BoxSizer(wx.HORIZONTAL)
		vbox_recognition.Add(hbox_lists, 1, wx.ALL | wx.EXPAND, 5)
		
		self.list_not_recognized = wx.ListCtrl(self.recognition_pane, wx.ID_ANY, style=wx.FULL_REPAINT_ON_RESIZE | wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
		self.list_not_recognized.SetBackgroundColour(wx.Colour(255, 201, 205))
		self.list_not_recognized.AppendColumn(_("Not Recognized"), format=wx.LIST_FORMAT_LEFT, width=200)
		hbox_lists.Add(self.list_not_recognized, 1, wx.ALL | wx.EXPAND, 5)
		
		self.list_recognized = wx.ListCtrl(self.recognition_pane, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
		self.list_recognized.SetBackgroundColour(wx.Colour(196, 255, 216))
		self.list_recognized.AppendColumn(_("Recognized"), format=wx.LIST_FORMAT_LEFT, width=200)
		hbox_lists.Add(self.list_recognized, 1, wx.ALL | wx.EXPAND, 5)
		
		self.list_selection = wx.ListCtrl(self.recognition_pane, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
		self.list_selection.AppendColumn(_("Selected"), format=wx.LIST_FORMAT_LEFT, width=400)
		vbox_recognition.Add(self.list_selection, 1, wx.ALL | wx.EXPAND, 10)
		
		hbox_save = wx.BoxSizer(wx.HORIZONTAL)
		vbox_recognition.Add(hbox_save, 0, wx.ALL | wx.EXPAND, 10)
		
		self.txt_name = wx.TextCtrl(self.recognition_pane, wx.ID_ANY, "")
		hbox_save.Add(self.txt_name, 3, wx.ALIGN_BOTTOM | wx.ALL, 5)
		
		self.save_btn = wx.Button(self.recognition_pane, wx.ID_ANY, _("Save"))
		self.save_btn.SetBackgroundColour(wx.Colour(70, 212, 110))
		self.save_btn.SetForegroundColour(wx.Colour(9, 40, 88))
		self.save_btn.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
		hbox_save.Add(self.save_btn, 0, wx.ALIGN_BOTTOM | wx.ALL, 5)
		
		self.recognition_pane.SetSizer(vbox_recognition)
		
		hbox_preview.AddGrowableRow(0)
		hbox_preview.AddGrowableCol(0)
		self.preview_pane.SetSizer(hbox_preview)
		
		self.splitter_window.SplitVertically(self.preview_pane, self.recognition_pane)
		
		self.sizer_1.AddGrowableRow(0)
		self.sizer_1.AddGrowableCol(0)
		self.SetSizer(self.sizer_1)
		self.sizer_1.Fit(self)
		self.sizer_1.SetSizeHints(self)
		
		if config.get('language') != 'he':
			self.SetLayoutDirection(wx.Layout_LeftToRight)
		
		self.Layout()
		self.Centre()
		
		# buttons Binds
		self.Bind(wx.EVT_BUTTON, self.test, self.start_btn)
		self.Bind(wx.EVT_BUTTON, self.test, self.save_btn)
		self.Bind(wx.EVT_SIZING, self.resize_preview_pane)
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.recognized_list_event, self.list_recognized)
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.not_recognized_list_event, self.list_not_recognized)
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selection_list_event, self.list_selection)
		self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.not_recognized_click, self.list_not_recognized)
		self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.selected_click, self.list_selection)
	
	# end wxGlade
	def not_recognized_list_event(self, event):
		name = self.list_not_recognized.GetItemText(event.GetIndex())
		self.preview_pdf("pdf/not_recognized/{}.pdf".format(name))
	
	def recognized_list_event(self, event):
		name = self.list_recognized.GetItemText(event.GetIndex())
		self.preview_pdf("pdf/recognized/{}.pdf".format(name))
		self.txt_name.Clear()
		self.txt_name.WriteText(str(name))
	
	def selection_list_event(self, event):
		name = self.list_selection.GetItemText(event.GetIndex())
		self.preview_pdf("pdf/not_recognized/{}.pdf".format(name))
	
	def not_recognized_click(self, event):
		text = self.list_not_recognized.GetItemText(event.GetIndex())
		self.list_not_recognized.DeleteItem(event.GetIndex())
		self.list_selection.InsertItem(event.GetIndex(), text)
	
	def selected_click(self, event):
		text = self.list_selection.GetItemText(event.GetIndex())
		self.list_selection.DeleteItem(event.GetIndex())
		self.list_not_recognized.InsertItem(event.GetIndex(), text)
		
	def test(self, event):
		self.start_btn.Disable()
		self.list_not_recognized.DeleteAllItems()
		self.list_recognized.DeleteAllItems()
		thread1 = threading.Thread(target=self.start)
		thread1.start()
	
	def resize_preview_pane(self, event):
		self.preview_image_size = self.preview_pane.GetSize()
	
	def preview_pdf(self, pdf):
		doc = fitz.open(pdf)
		print(doc.page_count)
		pix = doc[0].get_pixmap()
		if pix.alpha:
			bitmap = wx.Bitmap.FromBufferRGBA(pix.width, pix.height, pix.samples)
		else:
			bitmap = wx.Bitmap.FromBuffer(pix.width, pix.height, pix.samples)
		x, y = self.preview_image_size
		bitmap = self.scale_bitmap(bitmap, x, y)
		self.image_preview.SetBitmap(bitmap)
		self.image_preview.Layout()
		print("preview pdf")
		
	def preview_image(self):
		image = wx.Image(self.preview_image_path)
		bmp = wx.Bitmap(image)
		x, y = self.preview_image_size
		bmp = self.scale_bitmap(bmp, x, y)
		self.image_preview.SetBitmap(wx.Bitmap(bmp))
		self.image_preview.Layout()
	
	@staticmethod
	def scale_bitmap(bitmap, width, height):
		image = wx.Bitmap.ConvertToImage(bitmap)
		image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
		result = wx.Bitmap(image)
		return result
	
	@staticmethod
	def decode_barcodes(image):
		regex = re.compile(config['regex'])
		img = cv2.imread(image)
		decoded = pyzbar.decode(img)
		for bar in decoded:
			barcode_data = bar.data.decode("utf-8")
			if regex.match(barcode_data):
				return barcode_data
		return None
	
	def get_pdf_barcodes(self, pdf_file):
		with tempfile.TemporaryDirectory() as path:
			images = convert_from_path(pdf_file, dpi=600, fmt="jpeg", paths_only=True, thread_count=4, output_folder=path, poppler_path=poppler_path)
			for image in images:
				found = self.decode_barcodes(image)
				if found is not None:
					return found
		return
	
	def start(self):
		from glob import glob
		
		pdf_files = glob(config['input_folder'] + "\\*.pdf")
		not_recognized_folder = config['input_folder'] + "\\not_recognized"
		recognized_folder = config['input_folder'] + "\\recognized"
		Path(not_recognized_folder).mkdir(parents=True, exist_ok=True)
		Path(recognized_folder).mkdir(parents=True, exist_ok=True)
		Path(config['output_folder']).mkdir(parents=True, exist_ok=True)
		
		guage_length = len(pdf_files)
		print(guage_length)
		self.progress_gauge.SetRange(guage_length)
		progress = 0
		recognized = 0
		not_recognized = 0
		for pdf in pdf_files:
			progress += 1
			now = datetime.now()
			date_time = now.strftime("%d%m%y_%H_%M_%S")
			new_name = '{}.pdf'.format(date_time)
			
			barcode = self.get_pdf_barcodes(pdf)
			if barcode is not None:
				print(pdf, " ", barcode)
				new_name = '{}.pdf'.format(barcode)
				# copyfile(pdf, join(recognized_folder, new_name))
				move(pdf, join(recognized_folder, new_name))
				self.list_recognized.InsertItem(recognized, barcode)
				print(barcode)
				recognized += 1
			else:
				self.list_not_recognized.InsertItem(not_recognized, date_time)
				print(date_time)
				# copyfile(pdf, join(not_recognized_folder, new_name))
				move(pdf, join(not_recognized_folder, new_name))
				not_recognized += 1
			
			self.progress_gauge.SetValue(progress)
		self.start_btn.Enable()

# end of class MainFrame

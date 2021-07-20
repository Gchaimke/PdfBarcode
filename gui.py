from PIL import Image, ImageTk
import PySimpleGUI as Sg
import os.path
from pyzbar import pyzbar
from pdf2image import convert_from_path
from shutil import move
import tempfile
import cv2
import re
from pathlib import Path
from datetime import datetime
import configparser

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
    config.set("default", "tmp_folder", 'pdf\\tmp')
    config.set("default", "popper_path", 'poppler_21_03_0')
    config_file = open("config.ini", 'w')
    config.write(config_file)
    config_file.close()
    config.read('config.ini')

config = config['default']
poppler_path = config.get('popper_path')

tmp_folder = config.get('tmp_folder')
input_folder = config['input_folder']
output_folder = config['output_folder']
not_recognized_folder = tmp_folder + "\\not_recognized"

Path(tmp_folder).mkdir(parents=True, exist_ok=True)
Path(input_folder).mkdir(parents=True, exist_ok=True)
Path(not_recognized_folder).mkdir(parents=True, exist_ok=True)
recognized = []
not_recognized = []


def get_pdf_barcodes(pdf_file):
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(pdf_file, dpi=600, fmt="jpeg", paths_only=True, thread_count=4, output_folder=path,
                                   poppler_path=poppler_path)
        for image in images:
            file_name_path_recognized = os.path.join(Path().resolve(), tmp_folder, Path(pdf_file).stem+".jpeg")
            file_name_path_not_recognized = os.path.join(Path().resolve(), not_recognized_folder, Path(pdf_file).stem+".jpeg")

            found = decode_barcodes(image)
            if found is not None:
                move(image, file_name_path_recognized)
                return found
            else:
                move(image, file_name_path_not_recognized)
    return


def decode_barcodes(image):
    regex = re.compile(config['regex'])
    img = cv2.imread(image)
    decoded = pyzbar.decode(img)
    for bar in decoded:
        barcode_data = bar.data.decode("utf-8")
        if regex.match(barcode_data):
            return barcode_data
    return None


def recognize_barcodes():
    from glob import glob

    pdf_files = glob(input_folder + "\\*.pdf")
    for pdf in pdf_files:
        now = datetime.now()
        date_time = now.strftime("%d%m%y_%H_%M_%S")
        new_name = '{}.pdf'.format(date_time)

        barcode = get_pdf_barcodes(pdf)
        if barcode is not None:
            new_name = '{}.pdf'.format(barcode)
            move(pdf, os.path.join(output_folder, new_name))
            recognized.append(barcode)
        else:
            move(pdf, os.path.join(not_recognized_folder, new_name))
    return


def view_folder(path):
    if path == '':
        path = os.path.join(Path().resolve(), tmp_folder)
    try:
        # Get list of files in folder
        file_list = os.listdir(path)
    except:
        file_list = []

    file_names_list = [
        f
        for f in file_list
        if os.path.isfile(os.path.join(path, f))
        and f.lower().endswith((".png", ".gif", "jpeg", "jpg"))
    ]
    return file_names_list


# First the window layout in 2 columns
file_list_column = [
    [
        Sg.Text("Image Folder"),
        Sg.In(tmp_folder, size=(25, 1), enable_events=True, key="-FOLDER-"),
        Sg.FolderBrowse(),
    ],
    [
        Sg.Listbox(
            values=view_folder(''), enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [Sg.Text(size=(60, 1), key="-TOUT-")],
    [Sg.Image(key="-IMAGE-", enable_events=True)],
]

# ----- Full layout -----
layout = [
    [Sg.Button("Start", k='RECOGNIZE')],
    [Sg.Text("Choose an image from list:")],
    [
        Sg.Column(file_list_column),
        Sg.VSeperator(),
        Sg.Column(image_viewer_column),

    ],
    [Sg.Text(size=(-1, 1), key="-CHECKED-")]
]

window = Sg.Window("Image Viewer", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == Sg.WIN_CLOSED:
        break
    if event == "RECOGNIZE":
        recognize_barcodes()
        window["-CHECKED-"].update(recognized)
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        file_names = view_folder(folder)
        window["-FILE LIST-"].update(file_names)

    if event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                tmp_folder, values["-FILE LIST-"][0]
            )
            image = Image.open(filename)
            image.thumbnail((400, 400))
            photo_img = ImageTk.PhotoImage(image)
            window["-IMAGE-"].update(data=photo_img)
            window["-TOUT-"].update(values["-FILE LIST-"][0])
        except:
            pass

    if event == "-IMAGE-":
        current_file = window["-TOUT-"].get()
        if current_file in not_recognized:
            not_recognized.remove(current_file)
        else:
            not_recognized.append(current_file)
        window["-CHECKED-"].update(not_recognized)

window.close()

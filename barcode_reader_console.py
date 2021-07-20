from pyzbar import pyzbar
from pdf2image import convert_from_path
from os.path import join
from shutil import move
import tempfile
import argparse
import cv2
import re
from pathlib import Path
from datetime import datetime

poppler_path = r"poppler_21_03_0"


def get_pdf_barcodes(pdf_file):
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(pdf_file, dpi=600, fmt="jpeg", paths_only=True, thread_count=4, output_folder=path,
                                   poppler_path=poppler_path)
        for image in images:
            found = decode_barcodes(image)
            if found is not None:
                return found
    return


def decode_barcodes(image):
    regex = re.compile("^0[3,0][0,6,9]\d+$")
    img = cv2.imread(image)
    decoded = pyzbar.decode(img)
    for bar in decoded:
        barcode_data = bar.data.decode("utf-8")
        if regex.match(barcode_data):
            return barcode_data
    return None


def del_file(file):
    import os
    if os.path.exists(file):
        os.remove(file)
    else:
        print(file, " -The file does not exist")
    return


def get_args():
    parser = argparse.ArgumentParser(description='Scan pdfs and rename them according to '
                                                 'data in barcodes they contain.'
                                                 '\nTested on python 3.6.'
                                                 '\nRequirements: pip install pdf2image pyzbar')
    parser.add_argument('-i', '--input_folder', required=True, help='Where all pdf files take place.')
    parser.add_argument('-o', '--output_folder', required=True, help='Where to copy new renamed pdf files.')
    runtime_args = parser.parse_args()
    return runtime_args


if __name__ == "__main__":
    from glob import glob

    args = get_args()
    pdf_files = glob(args.input_folder+"\\*.pdf")
    not_recognized_folder = args.input_folder+"\\not_recognized"
    Path(not_recognized_folder).mkdir(parents=True, exist_ok=True)
    Path(args.output_folder).mkdir(parents=True, exist_ok=True)

    for pdf in pdf_files:
        now = datetime.now()
        date_time = now.strftime("%d%m%y_%H_%M_%S")
        new_name = '{}.pdf'.format(date_time)

        barcode = get_pdf_barcodes(pdf)
        if barcode is not None:
            print(pdf, " ", barcode)
            new_name = '{}.pdf'.format(barcode)
            move(pdf, join(args.output_folder, new_name))
            print(new_name)
        else:
            move(pdf, join(not_recognized_folder, new_name))

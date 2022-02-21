# PdfBarcode
Scan PDF Files for bracode template and raname file acordnly
# Setings
after first run if config.ini not exists, th program creates one wiht default settings:

[default]
input_folder = pdf
output_folder = pdf
regex = ^0[3,0][0,6,9]\d+$
wait = True
tmp_folder = tmp
poppler_path = poppler_21_03_0
language = en

language can be hebrew

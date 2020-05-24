from models import screenshoter
from time import sleep
import argparse
import logging

ap = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog='''\n
    This software has been made to automate taking screenshot and OCRing to text file.
    It is using Tesseract OCR v5.0.0

    Default is screenshot mode with 30s interval.
    To run in files use -m and -c left_corner_x left_corner_y width heigth. 
    
Examples:
    screenshOCR.py -t 15 -s
        Takes screenshot each 15s, save to .\\images\\ OCR to text.txt and include separator:
    
    screenshOCR.py -m 1 -c 0 0 300 300
        OCR all files from .\\images\\ 300x300 square starting from upper left corner of each image
        
        ''')
ap.add_argument('-m', '--mode', action='store_false', help="file mode")
ap.add_argument('-p', '--path', default='.\\images\\',help="files path, default is .\\images\\")
ap.add_argument('-c', '--corners', type=int, nargs=4, default=[0, 0, 0, 0], help="Img corners required with files mode eg. -c 0 0 1920 1080")
ap.add_argument('-t', '--time', type=int, default=30, help="Screenshot interval, default is 30s")
ap.add_argument('-o', '--output', default="text.txt", help="Output file, default is .\\text.txt")
ap.add_argument('-l', '--lang', default="pol", help="Language code. Check Tesseract Docs for codes. Default is Polish.")
ap.add_argument('-tp', '--tesseractpath', default="C:\\Program Files\\Tesseract-OCR\\tesseract.exe", help="path to tesseract.exe, default is C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
ap.add_argument('-d', '--delete', action='store_true', help="Delete screenshots (only screenshot mode)")
ap.add_argument('-s', '--separator', action='store_true', help="Separate images in text file")
args = vars(ap.parse_args())

#run app
def run(mode: bool, path: str, ocr_path: str, output_file: str, lang: str, interval: int, top_left_x: int, top_left_y: int, width: int, heigth: int, delete: bool, separator: bool):
    if mode:
        app = screenshoter(top_left_x=top_left_x, top_left_y=top_left_y, width=width, heigth=heigth, path=path, ocr_path=ocr_path, lang=lang, output_file=output_file, delete=delete, separator=separator)
        while True:
            app.start_screenshot()
            sleep(interval)
    else:
        try:
            if width == 0 or heigth == 0:
                raise Exception("Option -c is required for files mode")
            else:
                app = screenshoter(top_left_x=top_left_x, top_left_y=top_left_y, width=width, heigth=heigth, path=path, ocr_path=ocr_path, lang=lang, output_file=output_file, delete=delete, separator=separator)
                app.start_files()
                exit(0)
        except Exception as e:
            logging.critical(e)
            exit(1)

mode = args['mode']
path = args['path']
output_file = args['output']
ocr_path = args['tesseractpath']
lang = args['lang']
interval = args["time"]
top_left_x, top_left_y, width, heigth = args["corners"]
delete = args['delete']
separator = args['separator']

if __name__ == "__main__":
    run(mode, path, ocr_path, output_file, lang, interval, top_left_x, top_left_y, width, heigth, delete, separator)

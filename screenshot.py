
from PIL import ImageGrab, Image
from datetime import datetime
from time import sleep

import argparse
import os
from sys import exit

from pyautogui import position
import cv2
import numpy as np
import pytesseract

class screenshoter:
    a,b,c,d = 0, 0, 0, 0
    path = ""
    last_image_sum = 0
    output_file = ""
    ocr_path = ""
    lang = ""

    def __init__(self, output_file, ocr_path, path, lang='pol', a=0, b=0, c=0, d=0 ):
        if c == 0 or d == 0: #screenshot mode
            input("Set mouse cursor on upper left corner and press enter")
            self.a, self.b = position()
            input("OK. Now set mouse cursor on botton right corner and press enter")
            self.c, self.d = position()
        else:
            self.a = a
            self.b = b
            self.c = c
            self.d = d
        self.output_file=output_file
        self.ocr_path=ocr_path
        self.path=path
        self.lang=lang

    def _get(self):
        filename=str(datetime.now().strftime("%d_%m_%H_%M_%S"))
        im = ImageGrab.grab(bbox=(self.a,self.b,self.c,self.d))
        file_with_path = self.path + filename + ".png"
        im.save(file_with_path)
        return file_with_path

    def read(self):
        with open(self.output_file, "a",encoding='utf8') as f:
            filename=str(datetime.now().strftime("%d_%m_%H_%M_%S"))+'tmp.png'
            screenshot = self._get()
            image = cv2.imread(screenshot)
            if np.sum(image) != self.last_image_sum: 
                self.last_image_sum = np.sum(image)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                cv2.imwrite(filename, gray)
                pytesseract.pytesseract.tesseract_cmd = self.ocr_path
                text = pytesseract.image_to_string(Image.open(filename), lang=self.lang)
                #this line removesc screenshots, uncomment if you only need text (if ocr fails you will regred)
                #os.remove(screenshot)
                #this line removes files ocr is working on, grayscale and cropped
                os.remove(filename)
                f.write(text)
                print ("Text saved")
            else:
                print ("Skipping, image repeated")

    def read_files(self):
        #read files from dir
        files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]

        with open(self.output_file, "a", encoding='utf8') as f:
            for image in files:
                image = cv2.imread(self.path+image)
                image = image[self.b:self.d, self.a:self.c]
                filename=str(datetime.now().strftime("%d_%m_%H_%M_%S"))+'tmp.png'

                if np.sum(image) != self.last_image_sum: 
                    self.last_image_sum = np.sum(image)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                    cv2.imwrite(filename, gray)
                    pytesseract.pytesseract.tesseract_cmd = self.ocr_path
                    text = pytesseract.image_to_string(Image.open(filename), lang=self.lang)
                    f.write(text)
                    #this line removes files ocr is working on, grayscale and cropped
                    os.remove(filename)
                    print ("Text saved")
                else:
                    print ("Skipping, image repeated")



if __name__ == "__main__":
    #deal with args
    ap = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog='''\n
        This software has been made to automate taking screenshot and OCRing to text file.
        It is using Tesseract OCR v5.0.0

        Default is screenshot mode with 30s interval.
        To run in files use -m 1 and -c (corners).
        ''')
    ap.add_argument('-m', '--mode', choices=[0, 1], default=0, type=int, help="0 for screenshot, 1 for files. Default is screenshot mode.")
    ap.add_argument('-p', '--path', help="files path, default is .\\images\\")
    ap.add_argument('-c', '--corners', help="Img corners required with files mode eg. -c '0 0 1920 1080' ")
    ap.add_argument('-t', '--time', type=int, help="Screenshot interval, default is 30s")
    ap.add_argument('-o', '--output', help="output file, default is .\\text.txt")
    ap.add_argument('-l', '--lang', help="language, for codes check tesseract docs, default is polish")
    ap.add_argument('-tp', '--tensorpath', help="path to tesseract.exe, default is C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
    args = vars(ap.parse_args())
    
    #default settings
    output_file="text.txt"
    path='.\\images\\'
    ocr_path="C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    interval = 30
    lang = 'pol'
    a,b,c,d=0,0,0,0
    
    ocr = args['tensorpath']
    pth = args['path']
    outp = args['output']
    intrv = args["time"]
    l = args['lang']

    if ocr != None:
        ocr_path = ocr
    if pth != None:
        path = pth
    if outp != None:
        output_file = outp
    if intrv != None:
        interval = intrv
    if l != None:
        lang = l

    #run app
    def run(mode, path, ocr_path, output_file, a,b,c,d, lang):
        if mode:
            app = screenshoter(path=path, ocr_path=ocr_path, output_file=output_file)
            while True:
                app.read()
                sleep(interval)
        else:
            try:
                corners = args["corners"]
                print (corners)
                a,b,c,d = [int(i) for i in corners.split(" ")]
                if c == 0 or d == 0:
                    Exception("-c is required for file mode")
                else:
                    app = screenshoter(a=a, b=b, c=c, d=d, path=path, ocr_path=ocr_path, output_file=output_file)
                    app.read_files()
                    exit(0)
            except Exception as e:
                print (e)
                print ("-c argument is required when parsing from files! eg. -c '0 0 1920 1080'")
                exit(0)

    #mode = True if args['mode'] == None else False
    mode = not args['mode']
    run(mode, path, ocr_path, output_file, a,b,c,d, lang)

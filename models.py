from PIL import ImageGrab, Image
from datetime import datetime
from sys import exit
import os

from pyautogui import position
import numpy as np
import pytesseract
import cv2


class screenshoter:
    last_image_sum = 0

    def __init__(self, output_file, ocr_path, path, lang, a=0, b=0, c=0, d=0 ):
        if c == 0 or d == 0: #screenshot mode
            input("Set mouse cursor on upper left corner and press enter")
            self.a, self.b = position()
            input("OK. Now set mouse cursor on botton right corner and press enter")
            self.c, self.d = position()
        else: #file mode
            self.a, self.b, self.c, self.d = a, b, c, d

        self.output_file=output_file
        self.ocr_path=ocr_path
        self.path=path
        self.lang=lang

    def _takeScreenshot(self):
        filename=str(datetime.now().strftime("%d_%m_%H_%M_%S"))
        im = ImageGrab.grab(bbox=(self.a,self.b,self.c,self.d))
        file_with_path = self.path + filename + ".png"
        im.save(file_with_path)
        return file_with_path

    def read(self):
        with open(self.output_file, "a",encoding='utf8') as f:
            filename=str(datetime.now().strftime("%d_%m_%H_%M_%S"))+'tmp.png'
            screenshot = self._takeScreenshot()
            image = cv2.imread(screenshot)
            if np.sum(image) != self.last_image_sum: 
                self.last_image_sum = np.sum(image)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                cv2.imwrite(filename, gray)
                pytesseract.pytesseract.tesseract_cmd = self.ocr_path
                text = pytesseract.image_to_string(Image.open(filename), lang=self.lang)  
                #os.remove(screenshot) #this line removes screenshots 
                os.remove(filename) #this line removes files ocr image
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
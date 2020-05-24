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

    def __init__(self, output_file: str, ocr_path: str, path: str, lang: str, top_left_x: int, top_left_y: int, width: int, heigth: int, delete: bool, separator: bool):
        if width == 0 or heigth == 0: #screenshot mode
            input("Set mouse cursor on upper left corner and press enter")
            self.top_left_x, self.top_left_y = position()
            input("OK. Now set mouse cursor on botton right corner and press enter")
            self.width, self.heigth = position()
        else: #file mode
            self.top_left_x, self.top_left_y, self.width, self.heigth = top_left_x, top_left_y, width, heigth

        self.output_file=output_file
        self.ocr_path=ocr_path
        self.path=path
        self.lang=lang
        self.delete=delete
        self.separator=separator

    def _takeScreenshot(self):
        filename = f'{datetime.now():%d_%m_%H_%M_%S}_tmp.png'
        im = ImageGrab.grab(bbox=(self.top_left_x,self.top_left_y,self.width,self.heigth))
        file_with_path = self.path + filename + ".png"
        im.save(file_with_path)
        return file_with_path

    def start_screenshot(self):
        with open(self.output_file, "a",encoding='utf8') as f:
            filename = f'{datetime.now():%d_%m_%H_%M_%S}_tmp.png'
            screenshot = self._takeScreenshot()
            image = cv2.imread(screenshot)
            image_sum = np.sum(image)
            
            if image_sum != self.last_image_sum: 
                self.last_image_sum = image_sum
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                cv2.imwrite(filename, gray)
                pytesseract.pytesseract.tesseract_cmd = self.ocr_path
                text = pytesseract.image_to_string(Image.open(filename), lang=self.lang)  
                os.remove(filename) #image used by ocr
                if self.delete:
                    os.remove(screenshot) #real screenshot 
                f.write(text)
                if self.separator:
                    mark = "#" * 10
                    f.write("\n\n\n" + mark + " END OF IMAGE " + mark + "\n\n\n")
                print ("Text saved")
            else:
                print ("Skipping, image repeated")

    def start_files(self):
        #read files from dir
        files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]

        with open(self.output_file, "a", encoding='utf8') as f:
            for image in files:
                image = cv2.imread(self.path+image)
                image = image[self.top_left_y:self.heigth, self.top_left_x:self.width]
                filename=str(datetime.now().strftime("%d_%m_%H_%M_%S"))+'tmp.png'

                image_sum = np.sum(image)
                if image_sum != self.last_image_sum: 
                    self.last_image_sum = image_sum
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                    cv2.imwrite(filename, gray)
                    pytesseract.pytesseract.tesseract_cmd = self.ocr_path
                    text = pytesseract.image_to_string(Image.open(filename), lang=self.lang)
                    f.write(text)
                    if self.separator:
                        mark = "#" * 10
                        f.write( "\n\n\n" + mark + " END OF IMAGE " + mark + "\n\n\n")
                    os.remove(filename) #image used by ocr
                    print ("Text saved")
                else:
                    print ("Skipping, image repeated")
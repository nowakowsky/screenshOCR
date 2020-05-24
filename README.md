# screenshOCR

## This software has been made to take screenshots and OCR it to text file. It can also OCR all files from dir.

### It uses Tesseract OCR v5.0.0.

#### Examples:
    screenshOCR.py -t 15 -s
        Takes screenshot each 15s, save to .\\images\\ OCR to text.txt and include separator:
    
    screenshOCR.py -m 1 -c 0 0 300 300
        OCR all files from .\\images\\ 300x300 square starting from upper left corner of each image
    
    screenshotOCR.py -h 
        for all available options
# screenshOCR

# This software has been made to grab screenshot and OCR it to text file. It can also OCR all files from dir.

It uses Tesseract OCR v5.0.0.

usage: screenshot.py [-h] [-m {0,1}] [-p PATH] [-c CORNERS] [-t TIME] [-o OUTPUT] [-l LANG] [-tp TENSORPATH]

optional arguments:
  -h, --help            show this help message and exit
  -m {0,1}, --mode {0,1}
                        0 for screenshot, 1 for files. Default is screenshot mode.
  -p PATH, --path PATH  files path, default is .\images\
  -c CORNERS, --corners CORNERS
                        Img corners required with files mode eg. -c '0 0 1920 1080'
  -t TIME, --time TIME  Screenshot interval, default is 30s
  -o OUTPUT, --output OUTPUT
                        output file, default is .\text.txt
  -l LANG, --lang LANG  language, for codes check tesseract docs, default is polish
  -tp TENSORPATH, --tensorpath TENSORPATH
                        path to tesseract.exe, default is C:\Program Files\Tesseract-OCR\tesseract.exe

from models import screenshoter
from time import sleep
import argparse

if __name__ == "__main__":
    #deal with args
    ap = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog='''\n
        This software has been made to automate taking screenshot and OCRing to text file.
        It is using Tesseract OCR v5.0.0

        Default is screenshot mode with 30s interval.
        To run in files use -m 1 and -c (corners). ''')
    ap.add_argument('-m', '--mode', choices=[0, 1], default=0, type=int, help="0 for screenshot, 1 for files. Default is screenshot mode.")
    ap.add_argument('-p', '--path', help="files path, default is .\\images\\")
    ap.add_argument('-c', '--corners', help="Img corners required with files mode eg. -c '0 0 1920 1080' ")
    ap.add_argument('-t', '--time', type=int, help="Screenshot interval, default is 30s")
    ap.add_argument('-o', '--output', help="output file, default is .\\text.txt")
    ap.add_argument('-l', '--lang', help="language, for codes check tesseract docs, default is polish")
    ap.add_argument('-tp', '--tesseractpath', help="path to tesseract.exe, default is C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
    args = vars(ap.parse_args())
    
    #settings
    a,b,c,d = 0,0,0,0
    path = '.\\images\\' if args['path'] == None else args['path']
    output_file = "text.txt" if args['output'] == None else args['output']
    ocr_path = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" if args['tesseractpath'] == None else args['tesseractpath']
    lang = 'pol' if args['lang'] == None else args['lang']
    interval = 30 if args["time"] == None else int(args["time"])

    #run app
    def run(mode, path, ocr_path, output_file, a,b,c,d, lang):
        if mode:
            app = screenshoter(path=path, ocr_path=ocr_path, lang=lang, output_file=output_file)
            while True:
                app.read()
                sleep(interval)
        else:
            try:
                corners = args["corners"]
                a,b,c,d = [int(i) for i in corners.split(" ")]
                if c == 0 or d == 0:
                    Exception("-c is required for file mode")
                else:
                    app = screenshoter(a=a, b=b, c=c, d=d, path=path, ocr_path=ocr_path, lang=lang, output_file=output_file)
                    app.read_files()
                    exit(0)
            except Exception as e:
                print (e)
                exit(1)

    mode = not args['mode']
    run(mode, path, ocr_path, output_file, a,b,c,d, lang)

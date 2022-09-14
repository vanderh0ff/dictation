import glob
import re
import urllib.parse
import urllib.request
import os
import json

from PyPDF2 import PdfReader


def get_config():
    config = json.load(open('config.json'))
    if 'output_location' not in config or config['output_location'] == "":
        raise ValueError(
            "missing output_location in config.json, this should be the directory you want the mp3 files to output to")
    if 'file_location' not in config or config['file_location'] == "":
        raise ValueError(
            "missing file_location in config.json, this should list what directory the spelling weekly pdfs are in")
    global file_location
    global output_location
    file_location = config['file_location']
    output_location = config['output_location']
    if not os.path.exists(output_location):
        raise ValueError("the output location does not exist")
    if not os.path.exists(file_location):
        raise ValueError("the pdf file location does not exist")

def get_sound(f, i, question):
    url = 'https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=en&q=' + \
        urllib.parse.quote_plus(question)
    filename = f"{f.split('.')[0]}-{i}.mp3"
    urllib.request.urlretrieve(url, output_location + filename)
    pass


def text_to_sound():
    questions_regex = re.compile('[0-9]+\.[\s\w]+[\?\.\!]')
    files = glob.glob(file_location + "/*.txt")
    for f in files:
        n = 1
        for i, line in enumerate(open(f)):
            for match in re.finditer(questions_regex, line):
                get_sound(f, n, match.group())
                n += 1
            print(f)


def pdf_to_text():
    files = glob.glob(file_location + "/*.pdf")
    for f in files:
        reader = PdfReader(f)
        page = reader.pages[4]
        text = page.extract_text()
        # opens a text file with the same name as the pfd
        with open(f[:-3]+'txt', 'w') as o:
            o.writelines(text)


if __name__ == "__main__":
    get_config()
    pdf_to_text()
    text_to_sound()

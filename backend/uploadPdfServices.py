## Services with flask to upload a pdf file and save file in the server
from flask import Flask, request, send_file
from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

## Initialize flask app
app = Flask(__name__)
app.config["DEBUG"] = True

## Get environment variables
## Use export PATH_ROOT_FLASK="./backend/files/" in the terminal
path_root = os.environ.get('PATH_ROOT_FLASK')

@app.route('/uploadPdf', methods=['POST'])
def uploadPdf():
    ## get the file
    file = request.files['file']
    ## get the file name
    fileName = file.filename
    ## get the file extension
    fileExtension = fileName.split('.')[1]
    ## check if the file is a pdf
    if fileExtension == 'pdf':
        ## save the file
        file.save(path_root + fileName)
        ## return success
        readTextAndTranslate(path_root + fileName)
        return 'File saved successfully.'
    else:
        ## return error
        return 'Error: File must be a .pdf file'

## Read PDF and convert to text
def readPdfAndConverToText(pdfFile):
    pdfFileObj = open(pdfFile, 'rb')
    pdfReader = PdfReader(pdfFileObj)
    numPages = len(pdfReader.pages)
    for i in range(numPages):
        pageObj = pdfReader.pages[i]
        text = pageObj.extract_text()
        with open(path_root + 'text.txt', 'a', encoding='utf-8') as saveFile:
            saveFile.write(text)
        print('[LOG-readPdfAndConverToText] Text saved successfully.')
    pdfFileObj.close()
    with open(path_root + 'text.txt', 'r') as file:
        text = file.read().replace('\n', '')

    
    return text

def readTextAndTranslate(file):
    text = readPdfAndConverToText(file)    
    ## Translate text
    try:
        translated_text = translate_text(text, 'es')
        if translated_text:
            with open(path_root + 'translatedText.txt', 'w', encoding='utf-8') as saveFile:
                saveFile.write(translated_text)
            outputFile = file.split('pdf')[0]
            text_to_audio(translated_text,  outputFile + 'mp3')
            print('[LOG-readTextAndTranslate] Translation saved successfully.')
        else:
            print('[ERROR-readTextAndTranslate] Translation failed: No translation available.')
    except Exception as e:
        print('[ERROR-readTextAndTranslate] Translation failed:', e)

def translate_text(text, dest_lang):
    translated_text = ''
    chunk_size = 4000  # Adjust the chunk size as per your requirement
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    try: 
        for chunk in chunks:
            translated_chunk = GoogleTranslator(source='auto', target=dest_lang).translate(chunk)
            translated_text += translated_chunk + ' '
            print('[LOG-translate_text] Translation done.')
    except Exception as e:
        print('[ERROR-translate_text] Translation failed:', e)
    return translated_text.strip()

def text_to_audio(text, output_file):
    tts = gTTS(text=text, lang='es')
    try:
        tts.save(output_file)
        print('[LOG-text_to_audio] Audio saved successfully.')
    except Exception as e:
        print('[ERROR-text_to_audio] Audio failed:', e)

    

if __name__ == '__main__':
    app.run()


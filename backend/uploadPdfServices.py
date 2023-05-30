## Services with flask to upload a pdf file and save file in the server
from flask import Flask, request, send_file
from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator
from gtts import gTTS

app = Flask(__name__)
app.config["DEBUG"] = True

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
        file.save("files/" + fileName)
        ## return success
        readTextAndTranslate("files/" + fileName)
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
        print('Page: ', i)
        pageObj = pdfReader.pages[i]
        text = pageObj.extract_text()
        print(text)
        with open('text.txt', 'a', encoding='utf-8') as saveFile:
            saveFile.write(text)
        print('Text saved successfully.')
    pdfFileObj.close()
    with open('text.txt', 'r') as file:
        text = file.read().replace('\n', '')

    
    return text

def readTextAndTranslate(file):
    text = readPdfAndConverToText(file)    
    print(text)
    ## Translate text
    try:
        translated_text = translate_text(text, 'es')
        if translated_text:
            print("##############################################")
            print(translated_text)
            with open('translatedText.txt', 'w', encoding='utf-8') as saveFile:
                saveFile.write(translated_text)
            text_to_audio(translated_text, file.split('.')[0] + '.mp3')
            print('Translation saved successfully.')
        else:
            print('Translation failed: No translation available.')
    except Exception as e:
        print('Translation failed:', e)

def translate_text(text, dest_lang):
    translated_text = ''
    chunk_size = 4000  # Adjust the chunk size as per your requirement
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    for chunk in chunks:
        translated_chunk = GoogleTranslator(source='auto', target=dest_lang).translate(chunk)
        translated_text += translated_chunk + ' '
    
    return translated_text.strip()

def text_to_audio(text, output_file):
    tts = gTTS(text=text, lang='es')
    tts.save(output_file)

if __name__ == '__main__':
    app.run()


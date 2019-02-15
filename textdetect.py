import os
import subprocess
import tempfile


def ocr(path):
    temp = tempfile.NamedTemporaryFile(delete=False)
    process = subprocess.Popen(['D:/Tesseract-OCR/tesseract', path, temp.name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)    
    process.communicate()

    contents=None
    with open(temp.name + '.txt', 'r') as handle:
        contents = handle.read()

    #os.remove(temp.name + '.txt')
    #os.remove(temp.name)

    return contents

def refine(contents):
    S=""
    for i in contents:
        if(ord(i)>=ord('a') and ord(i)<=ord('z')):
            S+=i
        if(ord(i)>=ord('A') and ord(i)<=ord('Z')):
            S+=i
        if(ord(i)>=ord('0') and ord(i)<=ord('9')):
            S+=i
        
    return S

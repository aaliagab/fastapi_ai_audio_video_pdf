import os
from fastapi import APIRouter, File, UploadFile, Depends
import shutil
from PyPDF2 import PdfReader
from utils import get_auth

router_pdf = APIRouter()

file_path_pdf = "data/text_pdf.txt"

# Check if the directory exists, create it if not
directory = os.path.dirname(file_path_pdf)
if not os.path.exists(directory):
    os.makedirs(directory)

def get_list_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_pdf_text(pdf_file_path):
    with open(pdf_file_path, "rb") as f:
        pdf_reader = PdfReader(f)
        text = ""
        for i in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[i]
            text += page.extract_text()
    return text

def upload_file(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file

@router_pdf.post('/upload')
def upload(pdf: UploadFile, auth: dict = Depends(get_auth)):
    try:
        temp_pdf_path = os.path.join(os.getcwd(), pdf.filename)
        upload_file(pdf)
        result = get_pdf_text(temp_pdf_path)
        with open(file_path_pdf, "a") as file:
            file.write("PDF: "+pdf.filename+"\nContent from pdf: "+result+"\n\n")
        return result
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        print("Deleting temp pdf file: {}".format(temp_pdf_path))
        os.remove(temp_pdf_path)



import os
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
import shutil
from PyPDF2 import PdfReader
from utils import get_auth
from configurations.config import get_db
from sqlalchemy.orm import Session
from dao.content_dao import ContentDAO
from models.content import Content as SQLAlchemyContent
from dto.content_dto import Content, ContentCreate, ContentUpdate

router_pdf = APIRouter()

#def check_and_create_file_path(accesstoken_id):
#    file_path_pdf = f"data/{accesstoken_id}_pdf.txt"
#
#    # Check if the directory exists, create it if not
#    directory = os.path.dirname(file_path_pdf)
#    if not os.path.exists(directory):
#        os.makedirs(directory)
#    return file_path_pdf


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

@router_pdf.post('/content/upload')
def upload(pdf: UploadFile, source_id: str, accesstoken_id: str, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    if auth.get('auth').get('sources') == []:
        raise HTTPException(status_code=404, detail="Source not found for this account") 
    try:
        temp_pdf_path = os.path.join(os.getcwd(), pdf.filename)
        upload_file(pdf)
        text = get_pdf_text(temp_pdf_path)
        result = f"PDF TITLE: {pdf.filename}\nSOURCE ID: {source_id}\nACCESSTOKEN ID: {accesstoken_id}\nCONTENT: {text}\n\n"
        
        # Create content in db
        content = ContentCreate(source_id=source_id, access_id=accesstoken_id, title=pdf.filename,  phrase=text, status=1)
        db_content = SQLAlchemyContent(**content.dict())
        response = ContentDAO.create_content(db, db_content)

        #file_path_pdf = check_and_create_file_path(accesstoken_id)
        #with open(file_path_pdf, "a") as file:
        #    file.write(result)
        return text
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        print("Deleting temp pdf file: {}".format(temp_pdf_path))
        os.remove(temp_pdf_path)

#@router_pdf.post('/upload')
#def upload(pdf: UploadFile, auth: dict = Depends(get_auth)):
#    if auth.get('auth').get('sources') == []:
#        raise HTTPException(status_code=404, detail="Source not found for this account")
#    try:
#        temp_pdf_path = os.path.join(os.getcwd(), pdf.filename)
#        upload_file(pdf)
#        text = get_pdf_text(temp_pdf_path)
#        result = f"PDF TITLE: {pdf.filename}\nCONTENT: {text}\n\n"
#        
#        file_path_pdf = check_and_create_file_path("for_all_users")
#        with open(file_path_pdf, "a") as file:
#            file.write(result)
#        return result
#    except Exception as e:
#        return {'error': str(e)}, 500
#    finally:
#        print("Deleting temp pdf file: {}".format(temp_pdf_path))
#        os.remove(temp_pdf_path)




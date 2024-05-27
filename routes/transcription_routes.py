from ai.transcription import transcribe_audio,transcribe_video
import speech_recognition as sr
import os
import whisper
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse
import speech_recognition as sr
import shutil
from utils import get_auth
from configurations.config import get_db
from sqlalchemy.orm import Session
from dao.content_dao import ContentDAO
from models.content import Content as SQLAlchemyContent
from dto.content_dto import Content, ContentCreate, ContentUpdate


model_whisper_small = whisper.load_model("small")
#model_whisper_medium = whisper.load_model("medium")
router_transcription = APIRouter()

#def check_and_create_file_path(accesstoken_id, type):
#    file_path = f"data/{accesstoken_id}_{type}.txt"
#
#    # Check if the directory exists, create it if not
#    directory = os.path.dirname(file_path)
#    if not os.path.exists(directory):
#        os.makedirs(directory)
#    return file_path

#def check_and_create_file_path_forall(type):
#    file_path = f"data/for_all_users_{type}.txt"
#
#    # Check if the directory exists, create it if not
#    directory = os.path.dirname(file_path)
#    if not os.path.exists(directory):
#        os.makedirs(directory)
#    return file_path

def upload_file(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file

#ZONE TRANSCRIBE ENDPOINTS
@router_transcription.post('/ai/transcribe-audio-google')
def transcribe_audio_google(audio: UploadFile, auth: dict = Depends(get_auth)):
    if audio is None:
        return JSONResponse(content={'error': 'Audio file not provided'}, status_code=400)

    _, ext = os.path.splitext(audio.filename)
    if ext not in ('.wav'):
        return JSONResponse(content={'error': 'Invalid file format'}, status_code=400)

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio.file) as source:
            audio_data = recognizer.record(source)
            text_result = recognizer.recognize_google(audio_data)  # Utiliza Google Web Speech API para la transcripción

        return JSONResponse(content={'text_result': text_result}, status_code=200)
    except sr.UnknownValueError:
        return JSONResponse(content={'error': 'Audio could not be transcribed'}, status_code=400)
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)
    

@router_transcription.post('/ai/transcribe-audio-openai-small')
def transcribe_audio_openai_small(audio: UploadFile, auth: dict = Depends(get_auth)):    
    return transcribe_audio(model_whisper_small, upload_file(audio))

#@router_transcription.post('/ai/transcribe-audio-openai-medium')
#def transcribe_audio_openai_medium(audio: UploadFile):
#    return transcribe_audio(model_whisper_medium, upload_file(audio))



@router_transcription.post('/ai/transcribe-video-openai-small')
def transcribe_video_openai_small(video: UploadFile, auth: dict = Depends(get_auth)):    
    return transcribe_video(model_whisper_small, upload_file(video))

#ZONE CREATE CONTENT AUDIO ENDPOINTS
@router_transcription.post('/ai/content/from-audio-openai-small')
def from_audio_openai_small(audio: UploadFile, source_id: str, accesstoken_id: str, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):    
    if auth.get('auth').get('sources') == []:
        raise HTTPException(status_code=404, detail="Source not found for this account") 
    text = transcribe_audio(model_whisper_small, upload_file(audio))[0]['text_result']
    result = f"AUDIO TITLE: {audio.filename}\nSOURCE ID: {source_id}\nACCESSTOKEN ID: {accesstoken_id}\nCONTENT: {text}\n\n"
    
    # Create content in db
    content = ContentCreate(source_id=source_id, access_id=accesstoken_id, title=audio.filename,  phrase=text, status=1)
    db_content = SQLAlchemyContent(**content.dict())
    response = ContentDAO.create_content(db, db_content)

    #file_path = check_and_create_file_path(accesstoken_id,"audio")
    #with open(file_path, "a") as file:
    #    file.write(result)
    return response

#@router_transcription.post('/ai/allusers/from-audio-openai-small')
#def allusers_audio_openai_small(audio: UploadFile, auth: dict = Depends(get_auth)):    
#    if auth.get('auth').get('sources') == []:
#        raise HTTPException(status_code=404, detail="Source not found for this account") 
#    text = transcribe_audio(model_whisper_small, upload_file(audio))[0]['text_result']
#    result = f"AUDIO TITLE: {audio.filename}\nCONTENT: {text}\n\n"
#    
#    file_path = check_and_create_file_path_forall("audio")
#    with open(file_path, "a") as file:
#        file.write(result)
#    return result

#ZONE CREATE CONTENT VIDEO ENDPOINTS
@router_transcription.post('/ai/content/from-video-openai-small')
def from_video_openai_small(video: UploadFile, source_id: str, accesstoken_id: str, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):    
    if auth.get('auth').get('sources') == []:
        raise HTTPException(status_code=404, detail="Source not found for this account") 
    text = transcribe_video(model_whisper_small, upload_file(video))[0]['text_result']
    result = f"VIDEO TITLE: {video.filename}\nSOURCE ID: {source_id}\nACCESSTOKEN ID: {accesstoken_id}\nCONTENT: {text}\n\n"
    
    # Create content in db
    content = ContentCreate(source_id=source_id, access_id=accesstoken_id, title=video.filename,  phrase=text, status=1)
    db_content = SQLAlchemyContent(**content.dict())
    response = ContentDAO.create_content(db, db_content)

    #file_path = check_and_create_file_path(accesstoken_id,"video")
    #with open(file_path, "a") as file:
    #    file.write(result)
    return response

#@router_transcription.post('/ai/allusers/from-video-openai-small')
#def allusers_video_openai_small(video: UploadFile, auth: dict = Depends(get_auth)):    
#    if auth.get('auth').get('sources') == []:
#        raise HTTPException(status_code=404, detail="Source not found for this account") 
#    text = transcribe_video(model_whisper_small, upload_file(video))[0]['text_result']
#    result = f"VIDEO TITLE: {video.filename}\nCONTENT: {text}\n\n"
#    
#    file_path = check_and_create_file_path_forall("video")
#    with open(file_path, "a") as file:
#        file.write(result)
#    return result
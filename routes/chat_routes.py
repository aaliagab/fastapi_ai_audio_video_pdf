import os
import textwrap
import nest_asyncio
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from llama_index.core import GPTVectorStoreIndex, SimpleDirectoryReader, Settings, Document
from llama_index.llms.openai import OpenAI
from utils import get_auth
from configurations.config import get_db
from dao.content_dao import ContentDAO

# Aplicar nest_asyncio para asegurar el bucle de eventos correcto
nest_asyncio.apply()

# Cámbiala por tu API de OpenAI
os.environ["OPENAI_API_KEY"] = 'MY-API-KEY-FROM-OPENAI'

# Definir e instanciar el modelo
modelo = OpenAI(temperature=0, model="gpt-3.5-turbo")
Settings.llm = modelo
Settings.chunk_size = 512

router_chat = APIRouter()

@router_chat.post('/file/chat/query-question-from-chatgpt')
def query_question_from_chatgpt(question: str, auth: dict = Depends(get_auth)):   
    #Leer los documentos del directorio data
    data = SimpleDirectoryReader(os.path.join(os.path.dirname(__file__), "../data/")).load_data() 

    #Indexar el contenido de los documentos guardados antes en data
    index = GPTVectorStoreIndex.from_documents(data)

    query = question + "Use the pieces of context to answer the users question. \nIf you don't know the answer, just say that you don't know, don't try to make up an answer. \nPlease do not generate answer out of the context. \nResponde en español"
    response = index.as_query_engine().query(query)
    result = ''
    for frase in textwrap.wrap(response.response, width=100):
        result+=frase+"\n"
    return result

@router_chat.post('/db/chat/query-question-from-chatgpt')
def db_query_question_from_chatgpt(question: str, db: Session = Depends(get_db), auth: dict = Depends(get_auth)):
    user_data = auth.get('auth')
    sources = user_data.get('sources')
    access_tokens = user_data.get('access_tokens')

    # Obtener el contenido de la base de datos según el source_id y accesstoken_id del usuario
    contents = ContentDAO.get_contents_by_user(db, sources, access_tokens)

    # Crear una lista de objetos Document a partir del contenido
    documents = [Document(text=f"TITLE: {content.title}\nCONTENT: {content.phrase}\n\n") for content in contents]

    # Indexar el contenido de los documentos
    index = GPTVectorStoreIndex.from_documents(documents)

    query = question + "Use the pieces of context to answer the users question. \nIf you don't know the answer, just say that you don't know, don't try to make up an answer. \nPlease do not generate answer out of the context. \nResponde en español"
    response = index.as_query_engine().query(query)
    result = ''
    for frase in textwrap.wrap(response.response, width=100):
        result += frase + "\n"
    return result

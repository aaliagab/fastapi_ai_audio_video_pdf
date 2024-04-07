import os
from fastapi import APIRouter, BackgroundTasks
from llama_index.core import GPTVectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
import textwrap

router_chat = APIRouter()

# Cámbiala por tu API de OpenAI
os.environ["OPENAI_API_KEY"] = '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'

# Definir e instanciar el modelo
modelo = OpenAI(temperature=0, model="gpt-3.5-turbo")
Settings.llm = modelo
Settings.chunk_size = 512

@router_chat.post('/chat/query-question-from-chatgpt')
async def query_question_from_chatgpt(question: str, background_tasks: BackgroundTasks):
    # Leer los documentos del directorio data
    data = SimpleDirectoryReader(os.path.join(os.path.dirname(__file__), "../data/")).load_data()

    # Indexar el contenido de los documentos guardados antes en data
    index = GPTVectorStoreIndex.from_documents(data)

    query = question + "Use the pieces of context to answer the users question. \nIf you don't know the answer, just say that you don't know, don't try to make up an answer. \nPlease do not generate answer out of the context. \nResponde en español"

    # Ejecutar la consulta en segundo plano y obtener el resultado
    background_result = await run_query(index, query)

    # Devolver el resultado directamente desde aquí
    return {"result": background_result}

async def run_query(index, query):
    response = index.as_query_engine().query(query)
    result = ''
    for frase in textwrap.wrap(response.response, width=100):
        result += frase + "\n"
    return result

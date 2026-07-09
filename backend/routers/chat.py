from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models.schemas import ChatRequest, ChatResponse
from services.chat_service import chat
from services.voice import hablar, escuchar

#puerta de entrada de JARVIS. Recibe las peticiones HTTP y las pasa al chat_service 

router = APIRouter()

# Endpoint principal del chat
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request:ChatRequest):
    response = chat(request.session_id, request.message)
    return ChatResponse(response=response, session_id=request.session_id)

#JARVIS habla en voz alta
@router.post("/hablar")
async def hablar_endpoint(data: dict):
    texto = data.get("texto", "")
    if texto:
        hablar(texto)
    return JSONResponse({"OK": True})

#JARVIS escucha el micro
@router.post("/escuchar")
async def escuchar_endpoint():
    texto = escuchar(duracion=5)
    return JSONResponse({"texto": texto})


# APIRouter mini-servidor dentro de FastAPI, agrupa los endpoints relacionados con el chat
# el decorador @router.post(/chat) le dice a FastAPI que cuando llegue una peticion POST a api/chat ejecute la funcion
# response_model=ChatResponse hace que FastApi valide automaticamente la respuesta tiene el formato correcto, llama a la funcion chat del servicio y devuelve la respuesta
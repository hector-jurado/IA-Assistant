from pydantic import BaseModel

# frontend manda un mensaje chatRequest JARVIS resibe un mensaje de texto y un ID de session para saber quien lo manda
# ChatResponse JARVIS devuelve
# Base model pydantic hace la validacion automaticamente
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    session_id:str
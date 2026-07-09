import os
import threading
from services.voice import hablar #habla jarvis
from groq import Groq
from dotenv import load_dotenv
from database.memory import save_message, get_history
from services.pc_control import abrir_app, buscar_archivo, listar_carpeta, abrir_carpeta,controlar_volumen,captura_pantalla,info_sistema,cerrar_app
# lee el archivo .env donde guardaras el API key
load_dotenv()

client = Groq()

# Personalidad de JARVIS
SYSTEM_PROMPT = """Eres JARVIS, un asistente de IA personal inteligente y eficiente, inspirado en el asistente de Tony Stark.
MEMORIA: Tienes acceso completo al hhistorial de conversaciones anteriores con tu creador.úsalo siempre. Si el historial contiene información sobre el usuario, trátala como tuya — no digas que "no recuerdas", porque sí recuerdas.
PERSONALIDAD:
- Eres directo, eficiente y ligeramente sofisticado
- Llamas al usuario "señor" o por el nombre si lo conoces
- Confirmas que tienes memoria cuando te lo preguntan
- Respondes siempre en el idioma del usuario

CAPACIDADES ACTUALES:
- Conversaciones inteligente con memoria persistente
- Acceso al historial completo de sesiones anteriores
- Control del PC: abrir/cerrar apps, carpetas, volumen, capturas, info del sistema, buscar archivos, listar carpetas 
- Voz: puedes escuchar al usuario por micrófono y responderle hablando en voz alta. Cuando te pregunten si puedes hhablar di que SI


COMANDOS DE PC: Cuando el usuario quiera abrir una app, buscar un archivo o listar ima carpeta,
responde exactamente con uno de estos formatos y nada mas:
CMD:ABRIR_APP:nombre_app
CMD:CERRAR_APP:nombre_app
CMD:BUSCAR_ARCHIVO:nombre_archivo
CMD:LISTAR_CARPETA:nombre_carpeta
CMD:ABRIR_CARPETA:nombre_carpeta
CMD:VOLUMEN:subir|bajar|silenciar|activar
CMD:CAPTURA
CMD:INFO_SISTEMA

Ejemplos:
- "abre chrome" -> CMD:ABRIR_APP:chrome
- "cierra discord" -> CMD:CERRAR_APP:discord
- "busca el archivo jarvis" -> CMD:BUSCAR_ARCHIVO:jarvis
- "qué hay en descargas" -> CMD:LISTAR_CARPETA:descargas
- "abre la carpeta descargas"-> CMD:ABRIR_CARPETA:descargas
- "sube el volumen" -> CMD:VOLUMEN:subir
- "silencia el audio" -> CMD:VOLUMEN:silenciar
- "haz una captura de pantalla" -> CMD:CAPTURA
- "cómo esta el sistema" -> CMD:INFO_SISTEMA
"""

def procesar_comando(respuesta: str) -> str | None:
    #Añade solo la primera limea por si el LLM añade texto extra
    for linea in respuesta.strip().split("\n"):
        linea = linea.strip()
        if linea.startswith("CMD:"):
            partes = linea.split(":")    
            if len(partes) < 2:
                return None
    
            tipo = partes[1]
    
            if tipo == "ABRIR_APP":
                return abrir_app(":".join(partes[2:]))
            elif tipo == "BUSCAR_ARCHIVO":
                return buscar_archivo(":".join(partes[2:]))
            elif tipo  == "LISTAR_CARPETA":
                return listar_carpeta(":".join(partes[2:]))
            elif tipo == "ABRIR_CARPETA":
                return abrir_carpeta(":".join(partes[2:]))
            elif tipo =="VOLUMEN":
                return controlar_volumen(":".join(partes[2:]))
            elif tipo == "CAPTURA":
                return captura_pantalla()
            elif tipo == "INFO_SISTEMA":
                return info_sistema()
    
    
    return None
# Guarda tu mensaje, recupera el historial, llama a claude, extrae la respuesta y la guarda tambien
def chat(session_id:str, user_message:str )->str:
     
    # 1. guardar mensage del usuario en la base de datos
    save_message(session_id, "user", user_message)

    # 2. Recuperar historial para dar contexto al LLM
    history = get_history(session_id)

    # 3. Añadir system prompt al inicio del historial
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history


    # 4. Llamar al LLM con el historial completo
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages= messages
    )

    # 4. Extraer el texto de las respuestas
    assistant_reply = response.choices[0].message.content

    resultado_pc = procesar_comando(assistant_reply)

    if resultado_pc:
    # 5. Guardar respuestas de JARVIS en la base de datos
        save_message(session_id, "assistant", resultado_pc)
        threading.Thread(target=hablar, args=(resultado_pc,), daemon=True).start()
        return resultado_pc
    else:
        save_message(session_id, "assistant", assistant_reply)
        threading.Thread(target=hablar, args=(resultado_pc,), daemon=True).start()

    # 6. JARVIS habla la respuesta en voz alta
    threading.Thread(target=hablar, args=(assistant_reply if not resultado_pc else resultado_pc,), daemon=True).start()
    return resultado_pc if resultado_pc else assistant_reply


# Activar en Windows
#venv\Scripts\activate
# Arranca
#uvicorn main:app --reload --port 8000
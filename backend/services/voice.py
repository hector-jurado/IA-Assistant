import pyttsx3
import speech_recognition as sr
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import subprocess
import tempfile
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from dotenv import load_dotenv

load_dotenv()

client_el = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

VOICE_ID ="pNInz6obpgDQGcFmaJgB"
def hablar(texto: str):
    try:
        audio = client_el.text_to_speech.convert(
            voice_id=VOICE_ID,
            text=texto,
            model_id="eleven_multilingual_v2",
            output_format="pcm_16000"  # PCM en lugar de mp3
        )

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(b"RIFF")
            f.write((36 + len(b"")).to_bytes(4, 'little'))
            f.write(b"WAVEfmt ")
            f.write((16).to_bytes(4, 'little'))
            f.write((1).to_bytes(2, 'little'))
            f.write((1).to_bytes(2, 'little'))
            f.write((16000).to_bytes(4, 'little'))
            f.write((32000).to_bytes(4, 'little'))
            f.write((2).to_bytes(2, 'little'))
            f.write((16).to_bytes(2, 'little'))
            f.write(b"data")
            audio_bytes = b"".join(audio)
            f.write(len(audio_bytes).to_bytes(4, 'little'))
            f.write(audio_bytes)
            temp_path = f.name

        import winsound
        winsound.PlaySound(temp_path, winsound.SND_FILENAME)
        os.unlink(temp_path)

    except Exception as e:
        print(f"Error ElevenLabs: {str(e)}")
# ── Motor de voz (Text-to-Speech) ────────────────────────────────────────────
# engine = pyttsx3.init()

# def configurar_voz():
#     voices = engine.getProperty("voices")
#     #Voz en español
#     for voice in voices:
#         if "spanish" in voice.name.lower() or "es" in voice.id.lower():
#             engine.setProperty("voice", voice.id)
#             break
#     engine.setProperty("rate",175) #Velocidad de habla
#     engine.setProperty("volume",0.9) #Volume
# configurar_voz()

# def hablar(texto: str):
#     #JARVIS habla en voz alta
#     engine.say(texto)
#     engine.runAndWait()

# ── Reconocimiento de voz (Speech-to-Text) ───────────────────────────────────
def escuchar(duracion: int=5, sample_rate: int= 16000) -> str:
    try:
        print("Escuchando...")
        #Graba audio del micrófono

        audio_data = sd.rec(
            int(duracion * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )
        sd.wait() #Espera a que termine la grabacion

        #Guarda archivo temporal
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wav.write(f.name, sample_rate, audio_data)
            temp_path = f.name
        #Reconoce el audio con google speech recognition 
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_path) as source:
            audio = recognizer.record(source)

        os.unlink(temp_path) #Borra el archivo temporal

        texto = recognizer.recognize_google(audio, language="es-ES")
        print(f"Escuchando: {texto}")
        return texto

    except sr.UnknownValueError:
        return "" #No entendio
    except sr.RequestError as e:
        return "" #error de conexion google
    except Exception as e:
        print(f"Error al escuchar: {str(e)}")
        return ""
import os
import subprocess
import psutil
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from PIL import ImageGrab
from pathlib import Path
import datetime

# ── Lista blanca de aplicaciones permitidas ──────────────────────────────────

APPS_PERMITIDAS ={
    "chrome":           r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "navegador":        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "bloc de notas":    r"C:\Windows\System32\notepad.exe",
    "steam":            r"C:\Users\hecto\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Steam\Steam.lnk",
    "vscode":           r"C:\Users\hecto\OneDrive\Escritorio\Visual Studio Code.lnk",
    "discord":          r"C:\Users\hecto\AppData\Local\Discord\app-1.0.9242\Discord",
    "epic":             r"C:\Users\Public\Desktop\Epic Games Launcher.lnk",
    "explorador":       r"C:\Windows\explorer.exe",
    "calculadora":      r"C:\Windows\System32\calc.exe" ,
}

# ── Carpetas donde JARVIS puede buscar archivos ──────────────────────────────

CARPETAS_PERMITIDAS = [
    Path(r"C:\Users\hecto\Documents"),
    Path(r"C:\Users\hecto\Desktop"),
    Path(r"C:\Users\hecto\Downloads"),
    Path(r"C:\Users\hecto\jarvis"),
]

# ── Abrir aplicación ─────────────────────────────────────────────────────────
def abrir_app(nombre: str) -> str:
    nombre = nombre.lower().strip()

    # Buscar en la lista blanca
    ruta =APPS_PERMITIDAS.get(nombre)

    if not ruta:
        disponibles = ", ".join(APPS_PERMITIDAS.keys())
        return f"No tengo permiso para abrir '{nombre}'.Apps disponibles: {disponibles}"
    if not os.path.exists(ruta):
        return f"No encuentro '{nombre}' en la ruta configurada. Puede que no este instalada."
    
    try:
        subprocess.Popen([ruta])
        return f"Abriendo {nombre}..."
    except Exception as e:
        return f"Error al abrir {nombre}: {str(e)}"
        
# ── Buscar archivos ──────────────────────────────────────────────────────────
def buscar_archivo(nombre:str)-> str:
    nombre = nombre.lower().strip()
    resultados = []

    for carpeta in CARPETAS_PERMITIDAS:
        if not carpeta.exists():
            continue
    #   Busca recursivamente en las carpetas permitidas
    for archivo in carpeta.rglob("*"):
        if nombre in archivo.name.lower():
            resultados.append(str(archivo))
        if not resultados:
            return f"No encontré ningún archhivo con '{nombre}' en las carpetas permitidas."
     
    if len(resultados) > 10:
        resultados = resultados[:10]
        return f"Encontré mas de 10 resultados, mostrando los primeros:\n" + "\n".join(resultados)
    return f"Encontré {len(resultados)} archivo(s):\n" + "\n".join(resultados)
# ── Listar carpeta ───────────────────────────────────────────────────────────

def listar_carpeta(nombre: str)-> str:
    carpetas_map = {
        "documentos":   Path(r"C:\Users\hecto\Documents"),
        "escritorio":   Path(r"C:\Users\hecto\Desktop"),
        "descargas":    Path(r"C:\Users\hecto\Downloads"),
        "jarvis":       Path(r"C:\Users\hecto\jarvis"),
    }
    carpeta = carpetas_map.get(nombre.lower().strip())

    if not carpeta:
        disponibles = ", ".join(carpetas_map.keys())
        return f"Carpeta no permitida. Carpetas disponibles {disponibles}"
    if not carpeta.exists():
        return f"la carpeta '{nombre}' no existe"
    
    items = list(carpeta.iterdir())
    if not items:
        return f"la carpeta '{nombre}' está vacia."
    
    archivos = [f" 📄 {i.name}" if i.is_file() else f" 📁 {i.name}" for i in items[:20]]
    return f"Contenido de {nombre}:\n " + "\n".join(archivos)


def abrir_carpeta(nombre: str)-> str:
    carpetas_map = {
        "documentos":   Path(r"C:\Users\hecto\Documents"),
        "escritorio":   Path(r"C:\Users\hecto\Desktop"),
        "descargas":    Path(r"C:\Users\hecto\Downloads"),
        "jarvis":       Path(r"C:\Users\hecto\jarvis"),

    }

    carpeta = carpetas_map.get(nombre.lower().strip())

    if not carpeta:
        disponibles = ", ".join(carpetas_map.keys())
        return f"Carpeta no permitida. Carpetas disponibles: {disponibles}"
    
    if not carpeta.exists():
        return f"La carpeta '{nombre}' no existe."
    
    subprocess.Popen(["explorer", str(carpeta)])
    return f"Abriendo carpeta {nombre} en el explorador..."

# ── Volumen ──────────────────────────────────────────────────────────────────

def controlar_volumen(accion: str) -> str:
    try:
        # devices = AudioUtilities.GetSpeakers()
        # interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        # volume = cast(interface,POINTER(IAudioEndpointVolume))

        accion = accion.strip().lower()
        if accion == "silenciar":
            subprocess.run(["powershell", "-c", "$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]173)"],
                capture_output=True)
            return "Volumen silenciado."
        elif accion == "activar":
            subprocess.run(["powershell", "-c", "$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]173)"],
                capture_output=True)
            return "Volumen activado."
        elif accion == "subir":
            for _ in range(5):
                subprocess.run(["powershell", "-c", "$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]175)"],
                    capture_output=True)
                return f"Volumen subido."
        elif accion == "bajar":
            subprocess.run(["powershell", "-c", "$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]174)"],
                capture_output=True)
            return f"Volumen bajado."
        else:
            return "Acciòn de volumen no reconocida. Usa: subir, bajar, silenciar, activar"
    except Exception as e  :
        return f"Error controlando volumen: {str(e)}"  
        
# ── Captura de pantalla ───────────────────────────────────────────────────────

def captura_pantalla() -> str:
    try:
        ahora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = Path(r"C:\Users\hecto\OneDrive\Escritorio") / f"jarvis_captura_{ahora}.png"
        img = ImageGrab.grab()
        img.save(str(ruta))
        return f"Captura guardada en el escritorio como jarvis_captura_{ahora}.png"
    except Exception as e:
        return f"Error al capturar pantalla: {str(e)}"

# ── Info del sistema ──────────────────────────────────────────────────────────
def info_sistema() -> str:
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disco = psutil.disk_usage("C:\\")
        bateria = psutil.sensors_battery()
        
        ram_usada = round(ram.used / (1024**3), 1)
        ram_total = round(ram.total / (1024**3), 1)
        disco_libre = round(disco.free / (1024**3), 1)
        disco_total = round(disco.total / (1024**3), 1)

        bat_info = ""
        if bateria:
            estado = "cargando" if bateria.power_plugged else "descargando"
            bat_info = f"\n 🔋 Batería: {int(bateria.percent)}% ({estado})"
        return (
            f"📊 Estado del sistema:\n"
            f"⚡ CPU: {cpu}% de uso\n"
            f"🧠 RAM: {ram_usada}GB / {ram_total}GB ({ram.percent}% usado)\n"
            f"💾 Disco C: {disco_libre} GB libres de {disco_total}GB"
            f"{bat_info}"
        )
    except Exception as e:
        return f"Error obteniendo info del sistema: {str(e)}"

# ── Cerrar aplicación ─────────────────────────────────────────────────────────

APPS_CERRABLES = {
    "chrome":       "chrome.exe",
    "discord":      "Discord.exe",
    "spotify":      "Spotify.exe",
    "notepad":      "notepad.exe",
    "bloc de notas":"notepad.exe",
    "calculadora":  "Calculator.exe",
    "Steam":        "Steam.exe",
    "epic":         "epic.exe",
}

def cerrar_app(nombre: str) -> str:
    nombre = nombre.lower().strip()
    proceso = APPS_CERRABLES.get(nombre)

    if not proceso:
        disponibles = ", ".join(APPS_CERRABLES.keys())
        return f"No puedo cerrar '{nombre}'. Apps cerrables: {disponibles}"
    
    cerradas = 0
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == proceso:
            proc.kill()
            cerradas += 1
        
    if cerradas == 0:
        return f"{nombre} no estaba abierto"
    return f"{nombre} cerrado correctamente"
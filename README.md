# J.A.R.V.I.S. — Asistente de IA Personal

> *"Just a Rather Very Intelligent System"*

Asistente de inteligencia artificial personal con interfaz holográfica estilo HUD, inspirado en JARVIS de Iron Man. Combina un backend en Python/FastAPI con un modelo de lenguaje (Llama 3.3 70B vía Groq), memoria conversacional persistente y control del sistema operativo, todo servido a través de una interfaz futurista construida con HTML/CSS/JS.

🚧 **Proyecto en desarrollo activo** — funcional en su núcleo, con nuevas features añadiéndose constantemente.

---


## ✨ Características

- 💬 **Chat conversacional** con Llama 3.3 70B (Groq) a través de un prompt personalizado que le da personalidad a JARVIS.
- 🧠 **Memoria persistente** — recuerda los últimos 20 mensajes de la conversación (SQLite), manteniendo contexto entre interacciones.
- 🖥️ **Control del sistema**:
  - Abrir y buscar aplicaciones y carpetas
  - Control de volumen
  - Captura de pantalla
  - Información del sistema en tiempo real (uso de CPU y RAM)
- 🔊 **Síntesis de voz** con ElevenLabs *(en integración)*
- 🎛️ **Interfaz HUD holográfica** con animaciones, monitor de recursos en vivo y estética inspirada en ciencia ficción.

---
## Capturas de pantalla
<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/b58ecc27-cb46-4fc8-95be-33f52b6f9c58" />
<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/6b41dd63-2d85-46a2-a2a6-36995478d2fc" />


## 🛠️ Stack técnico

**Backend:**
- Python
- FastAPI
- SQLite
- Groq API (Llama 3.3 70B)
- ElevenLabs (TTS)

**Frontend:**
- HTML / CSS / JavaScript (vanilla)

---

## 📁 Estructura del proyecto

```
jarvis/
├── backend/
│   ├── main.py                 # Entry point de FastAPI
│   ├── database/
│   │   └── memory.py           # Gestión de memoria conversacional (SQLite)
│   ├── models/
│   │   └── schemas.py          # Modelos de datos (Pydantic)
│   ├── routers/
│   │   └── chat.py             # Endpoints de la API
│   └── services/
│       ├── chat_service.py     # Lógica del prompt y procesamiento del chat
│       ├── pc_control.py       # Control del sistema (apps, volumen, capturas...)
│       └── voice.py            # Síntesis de voz (ElevenLabs)
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js
```

---

## 🚀 Cómo ejecutarlo

### Backend

```bash
cd backend
venv\Scripts\activate          # Windows
uvicorn main:app --reload --port 8000
```

### Frontend

Abre `frontend/index.html` con **Live Server** (extensión de VS Code) o el servidor estático que prefieras.

### Variables de entorno

Crea un archivo `.env` en `backend/` con tus claves:

```
GROQ_API_KEY=tu_clave_aqui
ELEVENLABS_API_KEY=tu_clave_aqui
```

---

## 🗺️ Roadmap

- [ ] Resolver reproducción de audio (compatibilidad con Python 3.14)
- [ ] Sincronizar voz y efecto typewriter en el frontend
- [ ] Ampliar comandos de control del sistema
- [ ] Despliegue accesible fuera de local

---

## 📌 Estado

Proyecto personal en desarrollo continuo, usado como pieza central de portfolio en procesos de selección para roles junior de desarrollo/IA.

---

## Autor

**Hector Jurado**
[LinkedIn] · [Portfolio]

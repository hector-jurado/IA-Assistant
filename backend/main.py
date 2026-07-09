from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat
from database.memory import init_db

app = FastAPI(title="JARVIS API")

# Permite conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Inicializar base de datos al arrancar
@app.on_event("startup")
async def startup():
    init_db()

# Registrar router del chat
app.include_router(chat.router, prefix="/api")

# Endpoint de prueba
@app.get("/")
async def root():
    return {"status": "JARVIS online"}

# init_db() en el evento startup la base de datos se crea utomaticamente al arrancar jarvis
# middleware CORS permite que el frontend que correra en otro puerto pueda hablar con el backend
# prefix="/api" hace que todos los endpoints del chaht sean /api/chat
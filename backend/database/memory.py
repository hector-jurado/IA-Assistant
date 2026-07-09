import sqlite3
from pathlib import Path

DB_PATH = Path("jarvis_memory.db")

# crea la tabla
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
# guarda los mensajes enviados
def save_message(session_id: str, role:str, content:str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id,role,content)
    )
    conn.commit()
    conn.close()
# historial de la memoria
def get_history(session_id: str, limit: int = 20) -> list:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY created_at DESC LIMIT ? ",
        (session_id, limit)
    ). fetchall()
    conn.close()
    return[{"role": r[0], "content":r[1]} for r in reversed(rows)]


# DB_PATH: ruta donde se guarda el archivo de la base de datos
# init_db()crea la table donde se guardan los mensajes, cada fila tiene un ID unico, id de session el contenido del mensaje y la fecha
# get_history: recupera los ultimos 20 mensajes de tu session en orden cronologico reserved para el mas nuevo al mas viejo
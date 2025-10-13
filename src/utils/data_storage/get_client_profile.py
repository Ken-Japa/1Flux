import sqlite3
import json
from .database_config import DATABASE_PATH

def get_client_profile(client_name: str) -> dict:
    """
    Retorna o perfil de um cliente específico.

    Args:
        client_name (str): Nome do cliente.

    Returns:
        dict: Um dicionário representando o perfil do cliente, ou None se não encontrado.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client_profiles WHERE client_name = ?", (client_name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "client_name": row[1],
            "contact_info": row[2],
            "public_target": row[3],
            "tone_of_voice": row[4],
            "niche_examples": json.loads(row[5]),
            "status": row[6]
        }
    return None
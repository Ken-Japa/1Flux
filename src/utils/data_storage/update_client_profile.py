import sqlite3
import json
from .database_config import DATABASE_PATH

def update_client_profile(client_name: str, contact_info: str, public_target: str, tone_of_voice: str, niche_examples: list):
    """
    Atualiza um perfil de cliente existente no banco de dados.

    Args:
        client_name (str): O nome do cliente.
        contact_info (str): Informações de contato atualizadas do cliente.
        public_target (str): O público-alvo atualizado do cliente.
        tone_of_voice (str): O tom de voz preferido atualizado do cliente.
        niche_examples (list): Exemplos de nicho atualizados do cliente.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE client_profiles
        SET contact_info = ?, public_target = ?, tone_of_voice = ?, niche_examples = ?
        WHERE client_name = ?
    """, (contact_info, public_target, tone_of_voice, json.dumps(niche_examples), client_name))
    conn.commit()
    conn.close()
    print(f"Perfil do cliente '{client_name}' atualizado com sucesso.")
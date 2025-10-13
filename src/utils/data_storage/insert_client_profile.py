import sqlite3
import json
from .database_config import DATABASE_PATH

def insert_client_profile(client_name: str, contact_info: str, public_target: str,
                          tone_of_voice: str, niche_examples: list, status: str = 'active'):
    """
    Insere ou atualiza um perfil de cliente no banco de dados.
    Se o cliente já existir, o perfil será atualizado.

    Args:
        client_name (str): Nome único do cliente.
        contact_info (str): Informações de contato do cliente.
        public_target (str): Público-alvo do cliente.
        tone_of_voice (str): Tom de voz preferido do cliente.
        niche_examples (list): Exemplos de nicho (será armazenado como JSON string).
        status (str, optional): Status do cliente (ex: 'active', 'inactive', 'trial').
                                Padrão é 'active'.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO client_profiles (client_name, contact_info, public_target,
                                               tone_of_voice, niche_examples, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (client_name, contact_info, public_target, tone_of_voice,
          json.dumps(niche_examples), status))
    conn.commit()
    conn.close()
    print(f"Perfil do cliente '{client_name}' inserido/atualizado com sucesso.")
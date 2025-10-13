import sqlite3
import os
from .database_config import DATABASE_PATH

def init_db():
    """
    Conecta-se ao banco de dados SQLite e cria as tabelas 'client_briefs' e 'client_profiles'
    se elas não existirem. Garante que o diretório 'data' exista.
    """
    DATA_DIR = os.path.dirname(DATABASE_PATH)
    # Criar o diretório 'data' se ele não existir
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
    except Exception as e:
        print(f"[ERROR] Erro ao criar diretório 'data': {e}")
        raise # Re-raise a exceção para não mascarar o erro

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Tabela client_briefs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS client_briefs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            subniche TEXT,
            brief_data TEXT,
            generated_content TEXT,
            prompt_used TEXT,
            tokens_consumed INTEGER,
            api_cost_usd REAL,
            delivery_date TEXT,
            feedback_summary TEXT
        )
    """)

    # Tabela client_profiles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS client_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT UNIQUE NOT NULL,
            contact_info TEXT,
            public_target TEXT,
            tone_of_voice TEXT,
            niche_examples TEXT,
            status TEXT
        )
    """
    )
    conn.commit()
    conn.close()
    print("Banco de dados inicializado e tabelas criadas (se não existiam).")
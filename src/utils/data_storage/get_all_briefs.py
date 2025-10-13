import sqlite3
import json
from .database_config import DATABASE_PATH

def get_all_briefs() -> list:
    """
    Retorna todos os briefings e conteúdos gerados no banco de dados.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client_briefs")
    rows = cursor.fetchall()
    conn.close()

    briefs = []
    for row in rows:
        briefs.append({
            "id": row[0],
            "client_name": row[1],
            "subniche": row[2],
            "brief_data": json.loads(row[3]),
            "generated_content": json.loads(row[4]),
            "prompt_used": row[5],
            "tokens_consumed": row[6],
            "api_cost_usd": row[7],
            "delivery_date": row[8],
            "feedback_summary": row[9]
        })
    return briefs
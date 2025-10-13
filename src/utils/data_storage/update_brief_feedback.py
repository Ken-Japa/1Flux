import sqlite3
from .database_config import DATABASE_PATH

def update_brief_feedback(brief_id: int, feedback_summary: str):
    """
    Atualiza um registro de briefing com um resumo do feedback do cliente.

    Args:
        brief_id (int): O ID do briefing a ser atualizado.
        feedback_summary (str): O resumo do feedback do cliente.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE client_briefs
        SET feedback_summary = ?
        WHERE id = ?
    """, (feedback_summary, brief_id))
    conn.commit()
    conn.close()
    print(f"Feedback para o briefing ID {brief_id} atualizado com sucesso.")
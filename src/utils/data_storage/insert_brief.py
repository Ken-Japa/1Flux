import sqlite3
import json
from datetime import datetime
from .database_config import DATABASE_PATH

def insert_brief(client_name: str, subniche: str, brief_data: dict,
                 generated_content: dict, prompt_used: str, tokens_consumed: int,
                 api_cost_usd: float, delivery_date: str = None):
    """
    Insere um novo registro de briefing e conteúdo gerado no banco de dados.

    Args:
        client_name (str): Nome do cliente.
        subniche (str): Subnicho do cliente.
        brief_data (dict): Dados do briefing (será armazenado como JSON string).
        generated_content (dict): Conteúdo gerado (será armazenado como JSON string).
        prompt_used (str): O prompt exato usado para gerar o conteúdo.
        tokens_consumed (int): Número de tokens consumidos na geração.
        api_cost_usd (float): Custo da API em USD.
        delivery_date (str, optional): Data de entrega no formato YYYY-MM-DD.
                                       Padrão para a data atual se não fornecido.
    """
    if delivery_date is None:
        delivery_date = datetime.now().strftime('%Y-%m-%d')

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO client_briefs (client_name, subniche, brief_data, generated_content,
                                   prompt_used, tokens_consumed, api_cost_usd, delivery_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (client_name, subniche, json.dumps(brief_data), json.dumps(generated_content),
          prompt_used, tokens_consumed, api_cost_usd, delivery_date))
    conn.commit()
    conn.close()
    print(f"Briefing para '{client_name}' inserido com sucesso.")
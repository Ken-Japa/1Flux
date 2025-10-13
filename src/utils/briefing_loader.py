import json
import os

def load_briefing_from_json(filepath):
    """
    Carrega os dados do briefing de um arquivo JSON.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            briefing_data = json.load(f)
        return briefing_data
    except FileNotFoundError:
        print(f"Erro: Arquivo de briefing não encontrado em {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Arquivo JSON inválido em {filepath}")
        return None
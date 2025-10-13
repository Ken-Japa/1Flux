import json
import os

from .get_all_briefs import get_all_briefs

def export_all_briefs_to_json(output_filename: str = "all_briefs.json"):
    """
    Exporta todos os briefings armazenados no banco de dados para um arquivo JSON.

    Args:
        output_filename (str): O nome do arquivo JSON de saída.
    """
    briefs = get_all_briefs()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(BASE_DIR, '..', '..', '..', 'output_files', 'dados_clientes') # Ajuste para a pasta output_files
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(briefs, f, ensure_ascii=False, indent=4)
    print(f"Todos os briefings foram exportados para '{output_path}'")
import json
import sys
import os
from datetime import datetime

# Adiciona o diretório 'src' ao sys.path para que as importações funcionem
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from utils.html_generator.create_briefing_html import create_briefing_html

def main():
    """
    Script para gerar um arquivo HTML de briefing a partir de um arquivo JSON de conteúdo.
    Uso: python generate_html_from_json.py <caminho_para_json_de_conteudo>
    """
    if len(sys.argv) < 2:
        print("Uso: python generate_html_from_json.py <caminho_para_json_de_conteudo>")
        sys.exit(1)

    json_file_path = sys.argv[1]

    if not os.path.exists(json_file_path):
        print(f"Erro: Arquivo JSON não encontrado em {json_file_path}")
        sys.exit(1)

    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            content_json = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {e}")
        sys.exit(1)

    try:
        # Extrai o nome do cliente e a data de geração do nome do arquivo JSON
        file_name = os.path.basename(json_file_path)
        client_name_match = "_debug_" + file_name.split("_debug_")[1].split("_")[0]
        client_name = client_name_match.replace("_debug_", "").replace("_", " ").title() if "_debug_" in file_name else "Cliente Desconhecido"
        
        # A data pode ser extraída do nome do arquivo de debug
        date_match = file_name.split("_debug_")[1].split("_")[1]
        generation_date = date_match if len(date_match) == 8 and date_match.isdigit() else datetime.now().strftime("%Y%m%d")

        output_dir = os.path.join(os.path.dirname(__file__), 'output_files', 'briefings_testes')
        os.makedirs(output_dir, exist_ok=True)

        html_output_path = os.path.join(output_dir, f"briefing_{client_name.replace(" ", "_")}_{generation_date}.html")

        # Extrair informações adicionais do JSON para o sumário executivo
        target_audience = content_json.get('publico_alvo', '')
        tone_of_voice = content_json.get('tom_de_voz', '')
        marketing_objectives = content_json.get('objetivos_de_marketing', '')
        future_strategy = content_json.get('future_strategy', '')
        market_references = content_json.get('market_references', [])

        create_briefing_html(
            client_name=client_name,
            content_json=content_json,
            output_filename=html_output_path,
            target_audience=target_audience,
            tone_of_voice=tone_of_voice,
            marketing_objectives=marketing_objectives,
            future_strategy=future_strategy,
            market_references=market_references
        )
        print(f"HTML gerado com sucesso em: {html_output_path}")
    except Exception as e:
        print(f"Erro ao gerar o HTML: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
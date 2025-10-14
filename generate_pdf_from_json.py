import json
import sys
import os
from datetime import datetime

# Adiciona o diretório 'src' ao sys.path para que as importações funcionem
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from utils.pdf_generator.create_briefing_pdf import create_briefing_pdf


def main():
    """
    Script independente para geração de PDF a partir de um arquivo JSON de resposta da IA.
    Aceita o caminho do JSON como argumento e extrai parâmetros necessários do conteúdo JSON e do caminho do arquivo.
    """
    if len(sys.argv) < 2:
        print("Uso: python generate_pdf_from_json.py <caminho_para_json_de_conteudo>")
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

    # Carrega client_briefing.json para obter publico_alvo, tom_de_voz, objetivos_de_marketing
    client_briefing_path = os.path.join(os.path.dirname(__file__), 'client_briefing.json')
    client_briefing_data = {}
    if os.path.exists(client_briefing_path):
        try:
            with open(client_briefing_path, 'r', encoding='utf-8') as f:
                client_briefing_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Aviso: Erro ao decodificar client_briefing.json: {e}. Continuando sem dados do briefing do cliente.")
        except Exception as e:
            print(f"Aviso: Erro ao ler client_briefing.json: {e}. Continuando sem dados do briefing do cliente.")

    try:
        # Extrai modelo da IA a partir do caminho do arquivo (ex: output_files/respostas_IA/Gemini/...)
        model_name = os.path.basename(os.path.dirname(os.path.dirname(json_file_path)))
        client_name = content_json.get('client_name', 'Cliente Desconhecido')
        generation_date = content_json.get('generation_date', datetime.now().strftime("%Y%m%d"))

        output_dir = os.path.join(os.path.dirname(__file__), 'output_files', 'briefings_testes', model_name)
        os.makedirs(output_dir, exist_ok=True)

        pdf_output_path = os.path.join(output_dir, f"briefing_{client_name.replace(' ', '_')}_{generation_date}.pdf")

        # Extrai parâmetros necessários do JSON (compatível com main_gemini.py)
        target_audience = content_json.get('publico_alvo', client_briefing_data.get('publico_alvo', ''))
        tone_of_voice = content_json.get('tom_de_voz', client_briefing_data.get('tom_de_voz', ''))
        marketing_objectives = content_json.get('objetivos_de_marketing', client_briefing_data.get('objetivos_de_marketing', ''))
        posting_time = content_json.get('horario_de_postagem', '')
        future_strategy = content_json.get('future_strategy', '')
        market_references = content_json.get('market_references', None)
        suggested_metrics = content_json.get('metricas_de_sucesso_sugeridas', {}) # Adicionado

        create_briefing_pdf(
            client_name=client_name,
            content_json=content_json,
            output_filename=pdf_output_path,
            target_audience=target_audience,
            tone_of_voice=tone_of_voice,
            marketing_objectives=marketing_objectives,
            posting_time=posting_time,
            suggested_metrics=suggested_metrics # Adicionado
        )
        print(f"PDF gerado com sucesso em: {pdf_output_path}")
    except Exception as e:
        print(f"Erro ao gerar o PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
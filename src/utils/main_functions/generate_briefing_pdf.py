import json
import os
from datetime import datetime

from src.utils.pdf_generator.create_briefing_pdf import create_briefing_pdf

def generate_briefing_pdf(content_json: dict, client_name: str, output_dir: str, target_audience: str, tone_of_voice: str, marketing_objectives: str, model_name: str):
    """
    Gera um briefing em PDF com base no conteúdo JSON fornecido.

    Args:
        content_json (dict): O conteúdo JSON gerado pela IA.
        client_name (str): O nome do cliente.
        output_dir (str): O diretório de saída para o PDF.
        target_audience (str): O público-alvo do briefing.
        tone_of_voice (str): O tom de voz a ser utilizado no briefing.
        marketing_objectives (str): Os objetivos de marketing do briefing.
    """
    # Cria o diretório específico do modelo, se não existir
    model_output_dir = os.path.join(output_dir, model_name)
    os.makedirs(model_output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_filename = f"{model_name}_briefing_{client_name}_{timestamp}.pdf"
    output_filepath = os.path.join(model_output_dir, pdf_filename)

    suggested_metrics = content_json.get('metricas_de_sucesso_sugeridas', {})
    
    # Extrair datas do content_json e formatar o período
    start_date_str = content_json.get('start_date')
    end_date_str = content_json.get('end_date')

    formatted_period = ""
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            formatted_period = f"Período {start_date.strftime('%d/%m/%y')} a {end_date.strftime('%d/%m/%y')}"
        except ValueError:
            print("Aviso: Formato de data inválido no content_json. formatted_period não será gerado.")

    formatted_generation_date = datetime.now().strftime("%d de %B de %Y") # Gerar formatted_generation_date
    
    create_briefing_pdf(
        content_json=content_json,
        client_name=client_name,
        output_filename=output_filepath,
        target_audience=target_audience,
        tone_of_voice=tone_of_voice,
        marketing_objectives=marketing_objectives,
        suggested_metrics=suggested_metrics,
        model_name=model_name,
        formatted_period=formatted_period, # Passar formatted_period
        formatted_generation_date=formatted_generation_date # Passar formatted_generation_date
    )

    return output_filepath
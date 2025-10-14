import json
import os
from datetime import datetime
from src.utils.main_functions.generate_briefing_pdf import generate_briefing_pdf

# Carregar o conteúdo do client_briefing.json
with open('client_briefing.json', 'r', encoding='utf-8') as f:
    content_json = json.load(f)

# Definir parâmetros de exemplo
client_name = content_json.get('nome_do_cliente', 'Cliente Teste')
output_dir = os.path.join(os.getcwd(), 'output_files', 'briefings_testes')
target_audience = content_json.get('publico_alvo', 'Público Teste')
tone_of_voice = content_json.get('tom_de_voz', 'Tom Teste')
marketing_objectives = content_json.get('objetivos_de_marketing', 'Objetivos Teste')
model_name = 'Gemini'

# Chamar a função para gerar o PDF
output_filepath = generate_briefing_pdf(
    content_json=content_json,
    client_name=client_name,
    output_dir=output_dir,
    target_audience=target_audience,
    tone_of_voice=tone_of_voice,
    marketing_objectives=marketing_objectives,
    model_name=model_name
)

print(f"PDF gerado em: {output_filepath}")
import os
import json
from datetime import datetime
from dotenv import load_dotenv

from src.data_storage import init_db, insert_brief, get_client_profile, get_all_briefs, insert_client_profile
from src.content_generator_cohere import generate_content_for_client
from src.utils.pdf_generator.create_briefing_pdf import create_briefing_pdf
from src.html_generator import create_briefing_html
from src.utils.briefing_loader import load_briefing_from_json
from src.utils.prompt_logger import log_prompt
from src.config import COMPANY_NAME, BASE_DIR
from src.utils.main_functions.initialize_environment import initialize_environment
from src.utils.main_functions.collect_and_validate_briefing import collect_and_validate_briefing
from src.utils.main_functions.get_or_create_client_profile import get_or_create_client_profile
from src.utils.main_functions.generate_social_media_content_cohere import generate_social_media_content
from src.utils.main_functions.save_content_to_database import save_content_to_database
from src.utils.main_functions.generate_briefing_pdf import generate_briefing_pdf
from src.utils.main_functions.generate_briefing_html import generate_briefing_html
from src.utils.main_functions.display_success_message import display_success_message

def main():
    """
    Função principal que orquestra o fluxo de processamento do Concierge MVP.
    Inclui inicialização do DB, coleta de briefing, geração de conteúdo,
    salvamento no DB e geração de PDF.
    """
    print("\n--- Iniciando Concierge MVP ---")

    output_dir = initialize_environment()

    brief_data, nome_do_cliente, subnicho, informacoes_de_contato, \
    publico_alvo, tom_de_voz, exemplos_de_nicho, tipo_de_conteudo, \
    conteudos_semanais, objetivos_de_marketing = collect_and_validate_briefing()

    if nome_do_cliente is None:
        return

    client_profile = get_or_create_client_profile(
        nome_do_cliente,
        informacoes_de_contato,
        publico_alvo,
        tom_de_voz,
        exemplos_de_nicho
    )

    generated_content, prompt_used_for_content_generation, tokens_consumed, api_cost_usd = \
        generate_social_media_content(brief_data, nome_do_cliente, tipo_de_conteudo, conteudos_semanais, objetivos_de_marketing)

    if generated_content is None:
        return

    save_content_to_database(brief_data, nome_do_cliente, generated_content, prompt_used_for_content_generation, tokens_consumed, api_cost_usd, model_name="Cohere")

    # 6. Gerar PDF
    output_pdf_filename = generate_briefing_pdf(generated_content, nome_do_cliente, output_dir, publico_alvo, tom_de_voz, objetivos_de_marketing, model_name="Cohere")
    if output_pdf_filename is None:
        return

    # 7. Gerar HTML
    output_html_filename = generate_briefing_html(generated_content, nome_do_cliente, output_dir, model_name="Cohere")
    if output_html_filename is None:
        return

    display_success_message(output_pdf_filename, api_cost_usd)

if __name__ == "__main__":
    main()
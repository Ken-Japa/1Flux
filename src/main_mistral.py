import os
import json
import sys
from datetime import datetime
from pathlib import Path

# Adicionar o diretório pai ao path para importar módulos corretamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.prompt_manager.build_mistral_prompt import build_mistral_prompt
from src.llm_client.mistral_client import generate_text_content
from src.utils.html_generator.create_briefing_html import create_briefing_html
from src.utils.pdf_generator.create_briefing_pdf import create_briefing_pdf

def main():
    """
    Função principal que coordena o processo de consolidação de posts usando a Mistral.
    1. Carrega o perfil do cliente e diretrizes de nicho
    2. Carrega o resumo das ideias geradas por outras IAs
    3. Constrói o prompt para a Mistral
    4. Chama a API da Mistral
    5. Salva o prompt e a resposta
    6. Gera o PDF e HTML com os resultados
    """
    print("Iniciando processo de consolidação de posts com Mistral...")
    
    # Definir caminhos
    base_dir = Path(__file__).parent
    client_briefing_path = base_dir / "client_briefing.json"
    resumo_path = base_dir / "output_files" / "Resumo" / "Enviar" / "combined_summary_20251009_141117.json"
    logs_dir = base_dir / "output_files" / "logs_para_IA"
    respostas_dir = base_dir / "output_files" / "respostas_IA" / "Mistral"
    briefings_dir = base_dir / "output_files" / "briefings" / "Mistral"
    
    # Criar diretórios se não existirem
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(respostas_dir, exist_ok=True)
    os.makedirs(briefings_dir, exist_ok=True)
    
    # Verificar se o arquivo de resumo existe
    if not resumo_path.exists():
        print(f"Erro: Arquivo de resumo não encontrado em {resumo_path}")
        return
    
    # Carregar o briefing do cliente
    try:
        with open(client_briefing_path, 'r', encoding='utf-8') as f:
            client_briefing = json.load(f)
    except Exception as e:
        print(f"Erro ao carregar o briefing do cliente: {e}")
        return
    
    # Extrair informações do briefing
    client_profile = client_briefing.get("client_profile", {})
    niche_guidelines = client_briefing.get("niche_guidelines", {})
    content_type = client_briefing.get("content_type", "")
    weekly_themes = client_briefing.get("weekly_themes", [])
    weekly_goal = client_briefing.get("weekly_goal", "")
    campaign_type = client_briefing.get("campaign_type", "")
    strategic_analysis = client_briefing.get("strategic_analysis", {})
    
    # Extrair informações adicionais necessárias para o PDF
    publico_alvo = client_profile.get("publico_alvo", "")
    tom_de_voz = client_profile.get("tom_de_voz", "")
    objetivos_de_marketing = client_briefing.get("objetivos_de_marketing", [])
    
    # Construir o prompt para a Mistral
    prompt = build_mistral_prompt(
        client_profile=client_profile,
        niche_guidelines=niche_guidelines,
        content_type=content_type,
        weekly_themes=weekly_themes,
        weekly_goal=weekly_goal,
        campaign_type=campaign_type,
        strategic_analysis=strategic_analysis,
        resumo_path=str(resumo_path)
    )
    
    # Salvar o prompt enviado
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    prompt_filename = logs_dir / f"mistral_prompt_{timestamp}.txt"
    with open(prompt_filename, 'w', encoding='utf-8') as f:
        f.write(prompt)
    print(f"Prompt salvo em: {prompt_filename}")
    
    # Chamar a API da Mistral
    print("Chamando a API da Mistral...")
    response = generate_text_content(prompt)
    
    # Verificar se a resposta foi bem-sucedida
    if response["status"] == "success":
        # Salvar a resposta da IA
        response_filename = respostas_dir / f"mistral_response_{timestamp}.json"
        with open(response_filename, 'w', encoding='utf-8') as f:
            json.dump(response["generated_content"], f, ensure_ascii=False, indent=4)
        print(f"Resposta da IA salva em: {response_filename}")
        
        # Gerar HTML e PDF
        html_filename = briefings_dir / f"mistral_briefing_{timestamp}.html"
        pdf_filename = briefings_dir / f"mistral_briefing_{timestamp}.pdf"
        
        try:
            # Gerar HTML
            create_briefing_html(
                content_json=response["generated_content"],
                client_name=client_profile.get("nome_do_cliente", "Cliente"),
                output_filename=str(html_filename)
            )
            print(f"HTML gerado em: {html_filename}")
            
            # Gerar PDF
            create_briefing_pdf(
                content_json=response["generated_content"],
                client_name=client_profile.get("nome_do_cliente", "Cliente"),
                output_filename=str(pdf_filename),
                model_name="Mistral",
                target_audience=publico_alvo,
                tone_of_voice=tom_de_voz,
                marketing_objectives=objetivos_de_marketing
            )
            print(f"PDF gerado em: {pdf_filename}")
            
            print("Processo concluído com sucesso!")
            
        except Exception as e:
            print(f"Erro ao gerar HTML/PDF: {e}")
    else:
        print(f"Erro na resposta da IA: {response['message']}")

if __name__ == "__main__":
    main()
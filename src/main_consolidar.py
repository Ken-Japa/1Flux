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
from src.utils.prompt_manager.analyze_briefing_for_strategy import analyze_briefing_for_strategy

def find_latest_summary_file(directory):
    """
    Encontra o arquivo de resumo combinado mais recente em um diretório.
    
    Args:
        directory (Path): Caminho do diretório a ser pesquisado
    
    Returns:
        Path: Caminho completo do arquivo mais recente ou None se não encontrar
    """
    try:
        # Verificar se o diretório existe
        if not directory.exists():
            print(f"Diretório não encontrado: {directory}")
            return None
        
        # Listar todos os arquivos JSON no diretório que começam com 'combined_summary_'
        files = [f for f in directory.iterdir() if f.is_file() and f.name.startswith('combined_summary_') and f.name.endswith('.json')]
        
        if not files:
            print(f"Nenhum arquivo de resumo combinado encontrado em: {directory}")
            return None
        
        # Ordenar por data de modificação (mais recente primeiro)
        files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Retornar o caminho completo do arquivo mais recente
        return files[0]
    
    except Exception as e:
        print(f"Erro ao buscar arquivo de resumo mais recente: {str(e)}")
        return None

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
    base_dir = Path(__file__).parent.parent
    client_briefing_path = base_dir / "src" / "client_briefing.json"
    
    # Encontrar o arquivo de resumo combinado mais recente
    combined_summary_dir = base_dir / "output_files" / "Resumo" / "Enviar"
    resumo_path = find_latest_summary_file(combined_summary_dir)
    
    if not resumo_path:
        print("Erro: Nenhum arquivo de resumo combinado encontrado.")
        return

    logs_dir = base_dir / "output_files" / "logs_para_IA"
    respostas_dir = base_dir / "output_files" / "respostas_IA" / "Consolidado"
    briefings_dir = base_dir / "output_files" / "briefings" / "Consolidado"
    
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
    client_name = client_briefing.get("nome_do_cliente", "")
    client_profile = {
        "nome_do_cliente": client_briefing.get("nome_do_cliente", ""),
        "subnicho": client_briefing.get("subnicho", ""),
        "informacoes_de_contato": client_briefing.get("informacoes_de_contato", ""),
        "publico_alvo": client_briefing.get("publico_alvo", ""),
        "tom_de_voz": client_briefing.get("tom_de_voz", ""),
        "estilo_de_comunicacao": client_briefing.get("estilo_de_comunicacao", ""),
        "vocabulario_da_marca": client_briefing.get("vocabulario_da_marca", []),
        "exemplos_de_nicho": client_briefing.get("exemplos_de_nicho", []),
        "informacoes_adicionais": client_briefing.get("informacoes_adicionais", "")
    }
    niche_guidelines = {
        "subnicho": client_briefing.get("subnicho", ""),
        "exemplos_de_nicho": client_briefing.get("exemplos_de_nicho", [])
    }
    content_type = client_briefing.get("tipo_de_conteudo", "")
    weekly_themes_raw = client_briefing.get("conteudos_semanais", [])
    weekly_themes = [item.get("objetivo_do_conteudo_individual", "") for item in weekly_themes_raw]
    weekly_goal = client_briefing.get("objetivos_de_marketing", "")
    campaign_type = client_briefing.get("tipo_de_campanha", "")
    strategic_analysis = analyze_briefing_for_strategy(client_profile, niche_guidelines)

    
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
        response_filename = respostas_dir / f"mistral_response_{client_name}_{timestamp}.json"
        with open(response_filename, 'w', encoding='utf-8') as f:
            json.dump(response["generated_content"], f, ensure_ascii=False, indent=4)
        print(f"Resposta da IA salva em: {response_filename}")
        
        # Gerar HTML e PDF
        html_filename = briefings_dir / f"Relatorio-de-Postagem_{client_name}_{timestamp}.html"
        pdf_filename = briefings_dir / f"Relatorio-de-Postagem_{client_name}_{timestamp}.pdf"
        
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
                marketing_objectives=objetivos_de_marketing,
                suggested_metrics=response["generated_content"].get("metricas_de_sucesso_sugeridas", {})
            )
            print(f"PDF gerado em: {pdf_filename}")
            
            print("Processo concluído com sucesso!")
            
        except Exception as e:
            print(f"Erro ao gerar HTML/PDF: {e}")
    else:
        print(f"Erro na resposta da IA: {response['message']}")

if __name__ == "__main__":
    main()
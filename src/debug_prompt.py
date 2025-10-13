import json
import os

from .utils.prompt_manager.build_prompt import build_prompt

def debug_build_prompt():
    """
    Carrega o client_briefing.json, chama a função build_prompt e salva o resultado.
    """
    briefing_path = os.path.join(os.path.dirname(__file__), "client_briefing.json")
    output_path = os.path.join(os.path.dirname(__file__), "generated_prompt.txt")

    try:
        with open(briefing_path, 'r', encoding='utf-8') as f:
            client_briefing = json.load(f)
    except FileNotFoundError:
        print(f"Erro: O arquivo client_briefing.json não foi encontrado em {briefing_path}")
        return
    except json.JSONDecodeError:
        print(f"Erro: O arquivo client_briefing.json não é um JSON válido em {briefing_path}")
        return

    # Extrair os parâmetros necessários do client_briefing
    client_profile = client_briefing
    content_type = client_briefing.get("tipo_de_conteudo", "instagram_post") # Valor padrão se não encontrado
    campaign_type = client_briefing.get("tipo_de_campanha", "criativa") # Valor padrão se não encontrado

    # Definir valores mock para os outros parâmetros para depuração
    niche_guidelines = {}
    weekly_themes = ["Tema de Exemplo 1", "Tema de Exemplo 2"]
    weekly_goal = "Aumentar o engajamento em 15%"
    strategic_analysis = {
        "analise_swot": "Forças: Marca forte; Fraquezas: Pouca presença online; Oportunidades: Crescimento do mercado; Ameaças: Concorrência acirrada",
        "publico_alvo_detalhado": "Jovens adultos (25-35 anos) interessados em tecnologia e finanças."
    }

    # Chamar a função build_prompt
    generated_prompt = build_prompt(
        client_profile=client_profile,
        niche_guidelines=niche_guidelines,
        content_type=content_type,
        weekly_themes=weekly_themes,
        weekly_goal=weekly_goal,
        campaign_type=campaign_type,
        strategic_analysis=strategic_analysis
    )

    # Salvar o prompt gerado em um arquivo
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(generated_prompt)

    print(f"Prompt gerado e salvo em: {output_path}")

if __name__ == "__main__":
    debug_build_prompt()
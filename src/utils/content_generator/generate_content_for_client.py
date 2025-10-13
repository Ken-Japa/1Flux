import json
import re
from typing import List, Dict

from src.llm_client.gemini_client import generate_text_content
from src.prompt_manager import PromptManager
from src.utils.cache_manager import get_cache_key, get_from_cache, set_to_cache



def generate_content_for_client(
    client_data: Dict,
    niche_data: Dict,
    weekly_themes: List[str],
    weekly_goal: str,
    campaign_type: str,
    content_type: str
) -> Dict:
    """
    Gera conteúdo de mídia social para um cliente usando a API Google Gemini.

    Args:
        client_data (Dict): Dados do cliente.
        niche_data (Dict): Dados do nicho.
        weekly_themes (List[str]): Temas semanais para o conteúdo.
        weekly_goal (str): Objetivo semanal de marketing.
        campaign_type (str): O tipo de campanha (e.g., "lancamento", "autoridade").

    Returns:
        Dict: O conteúdo gerado para mídia social.
    """

    prompt_manager = PromptManager(client_data, niche_data)
    strategic_analysis = prompt_manager.analyze_briefing_for_strategy()
    prompt = prompt_manager.build_prompt(content_type=content_type, weekly_themes=weekly_themes, weekly_goal=weekly_goal, campaign_type=campaign_type, strategic_analysis=strategic_analysis)

    # Tenta carregar do cache primeiro
    cache_key_data = {
        "client_data": client_data,
        "niche_data": niche_data,
        "weekly_themes": weekly_themes,
        "weekly_goal": weekly_goal
    }
    cache_key = get_cache_key(cache_key_data)
    cached_content = get_from_cache(cache_key)
    if cached_content:
        print("Conteúdo carregado do cache.")
        return cached_content

    print("Gerando novo conteúdo com a API Gemini...")
    
    llm_response = generate_text_content(prompt)

    if llm_response["status"] == "success":
        generated_content = llm_response["generated_content"]
        set_to_cache(cache_key, generated_content)
        return {
            "status": "success",
            "generated_content": generated_content,
            "prompt_sent": prompt,
            "token_usage": {
                "estimated_input_tokens": len(prompt.split()),
                "estimated_cost_usd": (len(prompt.split()) / 1000) * 0.0002
            }
        }
    else:
        print("DEBUG: Entrando no bloco ELSE (erro).")
        print("DEBUG: llm_response['message'] no bloco else: " + str(llm_response.get('message', 'N/A')))
        print("Erro ao gerar conteúdo: " + str(llm_response.get('message', 'N/A')))
        return {"status": "error", "message": llm_response.get("message", "Erro desconhecido")}
from ...prompt_manager import PromptManager
from ...llm_client.gemini_client import generate_image_description

def generate_image_prompts(post_content: dict, client_profile: dict) -> dict:
    """
    Gera um prompt descritivo para uma IA de geração de imagens/vídeos com base no conteúdo de um post.

    Args:
        post_content (dict): Dicionário contendo o conteúdo de um post (ex: legenda_principal, formato_sugerido).
        client_profile (dict): Dicionário com o perfil do cliente (subnicho, tom_de_voz, publico_alvo).

    Returns:
        dict: Um dicionário contendo o prompt visual gerado, informações de tokens e custo.
    """
    prompt_manager = PromptManager(client_profile)
    prompt = prompt_manager.build_image_prompt(client_profile, post_content)

    estimated_tokens = prompt_manager.get_token_count(prompt)
    estimated_cost = (estimated_tokens / 1000) * 0.0002

    try:
        response_data = generate_image_description(prompt)
        if response_data["status"] == "success":
            visual_prompt = response_data["visual_prompt"]
        else:
            raise Exception(response_data["message"])

        return {
            "status": "success",
            "visual_prompt": visual_prompt,
            "token_usage": {
                "estimated_input_tokens": estimated_tokens,
                "estimated_cost_usd": estimated_cost
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "prompt_sent": prompt,
            "token_usage": {
                "estimated_input_tokens": estimated_tokens,
                "estimated_cost_usd": estimated_cost
            }
        }
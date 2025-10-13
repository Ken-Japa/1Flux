"""
Módulo para construção de prompts para resumo de posts.
"""

def build_summary_prompt(posts_data, ia_name):
    """
    Constrói o prompt para resumir os posts.
    
    Args:
        posts_data (dict): Dicionário contendo o array de posts a ser resumido
        ia_name (str): Nome da IA que gerou os posts (Gemini ou Cohere)
    
    Returns:
        str: Prompt formatado para envio à IA
    """
    # Construir o prompt base
    prompt = f"""Resuma em no máximo 4000-5000 caracteres (visando ~800 chars por post resumido) os posts a seguir gerados pela IA {ia_name}.

Diretrizes para o resumo:
- Título/Tema: Manter completo (são curtos).
- Legenda Principal: Resumir para 100-150 caracteres (ex: "Versão curta: [essência da legenda]").
- Variações/Hashtags: Resumir para 1-2 itens mais relevantes.
- Manter a estrutura JSON original, apenas reduzindo o conteúdo.
- Preservar os campos mais importantes como "titulo", "tema", "legenda_principal" (resumida), "hashtags" (reduzidos).

Aqui estão os posts a serem resumidos:
"""

    # Adicionar os posts ao prompt
    import json
    prompt += json.dumps(posts_data, ensure_ascii=False, indent=2)
    
    # Adicionar instruções finais
    prompt += """

Retorne APENAS o JSON resumido, seguindo EXATAMENTE este formato:
{
  "posts": [
    {
      "titulo": "Título completo do post",
      "tema": "Tema completo",
      "legenda_principal": "Versão resumida da legenda principal (100-150 caracteres)",
      "hashtags": ["hashtag1", "hashtag2"],
      "post_strategy_rationale": "Razão para a escolha da estratégia de postagem",
      "micro_briefing": "Um pequeno briefing resumo do post",
      "cta_individual": "Chamada para ação específica para este post.",
      "interacao": "Formas de como aumentar a interação com este post."
    },
    // outros posts seguindo o mesmo formato
  ]
}

IMPORTANTE:
1. Mantenha a estrutura exata do JSON com o campo "posts" contendo o array
2. Cada post DEVE conter pelo menos os campos: titulo, tema, legenda_principal e hashtags
3. Não adicione campos extras que não existam no JSON original
4. O JSON deve ser válido e parseable (sem comentários, sem trailing commas)
5. Retorne APENAS o JSON, sem texto adicional antes ou depois
"""
    
    return prompt
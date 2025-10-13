def build_image_prompt(client_profile: dict, post_content: dict) -> str:
    """
    Constrói um prompt detalhado para uma IA de geração de imagens/vídeos com base no conteúdo do post.

    Args:
        client_profile (dict): Dicionário contendo o perfil do cliente.
        post_content (dict): Dicionário contendo o conteúdo de um post (ex: legenda_principal, formato_sugerido).

    Returns:
        str: O prompt visual detalhado para a IA de geração de imagens.
    """
    nome_do_cliente = client_profile.get('nome_do_cliente', 'cliente')
    subnicho = client_profile.get('subnicho', 'geral')
    tom_de_voz = client_profile.get('tom_de_voz', 'neutro')
    publico_alvo = client_profile.get('publico_alvo', 'amplo')

    main_caption = post_content.get('legenda_principal', '')
    suggested_format = post_content.get('sugestao_formato', '')

    prompt_parts = [
        f"Crie um prompt visual detalhado para uma IA de geração de imagens/vídeos.",
        f"O objetivo é gerar uma imagem ou vídeo que complemente o seguinte conteúdo de post para {nome_do_cliente} (subnicho: {subnicho}):",
        f"Legenda Principal: {main_caption}",
        f"Formato Sugerido: {suggested_format}",
        f"O tom de voz geral é {tom_de_voz} e o público-alvo é {publico_alvo}.",
        "Considere os seguintes elementos para o prompt visual:",
        "- Cenário e ambiente (interno/externo, dia/noite, localização específica).",
        "- Elementos visuais principais (pessoas, objetos, paisagens).",
        "- Estilo artístico (realista, cartoon, ilustração, 3D, fotografia).",
        "- Cores e iluminação (paleta de cores, tipo de luz).",
        "- Emoções e atmosfera que a imagem deve transmitir.",
        "- Composição e enquadramento (close-up, plano geral, ângulo).",
        "- Qualquer texto ou sobreposição que possa ser incluído na imagem (se aplicável).",
        "O prompt deve ser conciso, claro e rico em detalhes descritivos para guiar a IA de imagem/vídeo."
    ]

    return "\n".join(prompt_parts)
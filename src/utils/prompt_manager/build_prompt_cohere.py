import json
from .campaign_narrative_generator import generate_campaign_narrative
from ...metric_suggester import suggest_metrics

def build_prompt_cohere(client_profile: dict, niche_guidelines: dict, content_type: str, weekly_themes: list[str], weekly_goal: str, campaign_type: str, strategic_analysis: dict = None) -> str:
    """
    Constrói o prompt completo para a API do Gemini, combinando o perfil do cliente, diretrizes de nicho, contexto semanal e instruções de formato.

    Args:
        client_profile (dict): Dicionário contendo o perfil do cliente (subnicho, tom_de_voz, publico_alvo, objetivos_gerais).
        niche_guidelines (dict): Dicionário contendo diretrizes específicas do nicho.
        content_type (str): O tipo de conteúdo a ser gerado (ex: 'instagram_post').
        weekly_themes (list[str]): Uma lista de temas a serem abordados na semana.
        weekly_goal (str): O objetivo principal do conteúdo para a semana.
            campaign_type (str): O tipo de campanha (ex: 'autoridade').
            strategic_analysis (dict): O resultado da análise estratégica do briefing.

    Returns:
        str: O prompt completo formatado para a API do Gemini.
    """

    # Coleta de dados do perfil do cliente e diretrizes do nicho, tratando valores vazios
    nome_do_cliente = client_profile.get("nome_do_cliente", "")
    subnicho = client_profile.get("subnicho", "")
    tom_de_voz = client_profile.get("tom_de_voz", "")
    estilo_de_comunicacao = client_profile.get("estilo_de_comunicacao", "")
    vocabulario_da_marca = client_profile.get("vocabulario_da_marca", [])
    publico_alvo = client_profile.get("publico_alvo", "")
    objetivos_de_marketing = client_profile.get("objetivos_de_marketing", "")
    exemplos_de_nicho = client_profile.get("exemplos_de_nicho", [])
    canais_de_distribuicao = client_profile.get("canais_de_distribuicao", [])
    topicos_principais = client_profile.get("topicos_principais", [])
    palavras_chave = client_profile.get("palavras_chave", [])
    chamada_para_acao = client_profile.get("chamada_para_acao", "")
    restricoes_e_diretrizes = client_profile.get("restricoes_e_diretrizes", "")
    informacoes_adicionais = client_profile.get("informacoes_adicionais", "")
    referencias_de_concorrentes = client_profile.get("referencias_de_concorrentes", [])
    referencias_de_estilo_e_formato = client_profile.get("referencias_de_estilo_e_formato", [])
    posts_anteriores = client_profile.get("posts_anteriores", [])

    # Sugerir métricas com base no tipo de campanha e objetivos de marketing
    sugerir_metricas = suggest_metrics(campaign_type, objetivos_de_marketing)

    # Adicionar diretrizes de nicho, se existirem
    if niche_guidelines:
        for key, value in niche_guidelines.items():
            if isinstance(value, list):
                informacoes_adicionais += f" {key}: {', '.join(value)}."
            else:
                informacoes_adicionais += f" {key}: {value}."

    # System Message: Define o papel da IA
    system_message = f"Você é um copywriter especializado em mídias sociais."
    if subnicho:
        system_message += f" O nicho é {subnicho}."
    if niche_guidelines:
        if 'subnicho' in niche_guidelines and niche_guidelines['subnicho']:
            system_message += f" para {niche_guidelines['subnicho']}."
        if 'exemplos_de_nicho' in niche_guidelines and niche_guidelines['exemplos_de_nicho']:
            exemplos_str = ', '.join(niche_guidelines['exemplos_de_nicho'])
            system_message += f" Atuando sob as diretrizes de nicho: {exemplos_str}."
    system_message += f" Compreenda as nuances e particularidades deste segmento para gerar conteúdo.Seu objetivo é criar conteúdo altamente engajador, viral e relevante para o público-alvo do cliente."

    # User Message: Combina todas as informações para criar uma instrução detalhada
    user_message_parts = []
    if canais_de_distribuicao:
        canais_str = ', '.join(canais_de_distribuicao)
        user_message_parts.append(f"Com base no perfil do cliente e nas diretrizes do nicho, crie conteúdo para os seguintes canais: {canais_str}.")
    elif content_type:
        user_message_parts.append(f"Com base no perfil do cliente e nas diretrizes do nicho, crie conteúdo para {content_type}.")

    user_message_parts.append("Evite soar como uma IA, busque um estilo de texto humanizado, evite clichês de copy genérica.")

    user_message_parts.append("\n**Perfil do Cliente:**")
    if nome_do_cliente:
        user_message_parts.append(f"- Nome do Cliente: {nome_do_cliente}")
    if tom_de_voz:
        user_message_parts.append(f"- Tom de Voz: {tom_de_voz}")
    if estilo_de_comunicacao and estilo_de_comunicacao.strip():
        user_message_parts.append(f"- Busque criar o texto como se fosse: {estilo_de_comunicacao}")
    if vocabulario_da_marca and len(vocabulario_da_marca) > 0:
        user_message_parts.append(f"- O cliente costuma usar o vocabulário e ou frases como: {', '.join(vocabulario_da_marca)}. Busque adaptar seu texto ao estilo do cliente de se comunicar.")
    if publico_alvo:
        user_message_parts.append(f"- Público-Alvo: {publico_alvo}")

    # Análise Estratégica Inicial
    user_message_parts.append("\n**Análise Estratégica Inicial:**")
    if referencias_de_concorrentes:
        user_message_parts.append(f"- Análise de Concorrentes/Referências: Considere o estilo e as estratégias de conteúdo dos seguintes concorrentes/referências: {', '.join(referencias_de_concorrentes)}. Identifique oportunidades e diferenciais.")
    if informacoes_adicionais:
        user_message_parts.append(f"- Informações Adicionais e Diretrizes Específicas: {informacoes_adicionais}. Incorpore essas informações para refinar a estratégia de conteúdo.")

    user_message_parts.append("\n**Informações Estratégicas do Briefing:**")

    if objetivos_de_marketing:
        user_message_parts.append(f"- Objetivos de Marketing: {objetivos_de_marketing}")
    if canais_de_distribuicao:
        user_message_parts.append(f"- Canais de Distribuição: {', '.join(canais_de_distribuicao)}")
    if topicos_principais:
        user_message_parts.append(f"- Tópicos Principais: {', '.join(topicos_principais)}")
    if palavras_chave:
        user_message_parts.append(f"- Palavras-Chave: {', '.join(palavras_chave)}")
    if chamada_para_acao:
        user_message_parts.append(f"- Chamada para Ação (CTA): {chamada_para_acao}")
    if restricoes_e_diretrizes:
        user_message_parts.append(f"- Restrições e Diretrizes: {restricoes_e_diretrizes}")
    if posts_anteriores:
        user_message_parts.append("\n**Posts Anteriores:**")
        user_message_parts.append("Considere os seguintes posts já publicados e evite repetir temas ou abordagens de forma idêntica. Busque originalidade e complementariedade.")
        for post in posts_anteriores:
            user_message_parts.append(f"- Tema: {post.get('tema', 'Não especificado')}")
    if referencias_de_concorrentes:
        user_message_parts.append(f"- Concorrentes/Referências: {', '.join(referencias_de_concorrentes)}")
    if referencias_de_estilo_e_formato:
        user_message_parts.append(f"- Referências de Estilo e Formato: {', '.join(referencias_de_estilo_e_formato)}")

    if weekly_themes or weekly_goal:
        user_message_parts.append("\n**Contexto Semanal:**")
        if weekly_themes:
            user_message_parts.append(f"- Temas da Semana: {', '.join(weekly_themes)}")
        if weekly_goal:
            user_message_parts.append(f"- Objetivo Semanal: {weekly_goal}")

    user_message_parts.append("\n**Instruções de Formato:**")
    user_message_parts.append("Crie uma campanha semanal *coesa e com narrativa progressiva*, composta por 5 ideias de posts. Para cada post, inclua:")
    user_message_parts.append(" Os 5 Posts serão postados na seguinte ordem: sexta, sábado, domingo, segunda e quarta. Baseado no nicho, objetivo e nos dias da semana, retorne também um horário recomendado para postagem.")
    user_message_parts.append(" Busque se possivel inserir stroytelling ou casos ficticios no texto. Busque também inserir dados concretos, números ou estatísticas pertinentes mesmo que sejam aproximados no texto se fizer sentido.")
    user_message_parts.extend(generate_campaign_narrative(campaign_type))
    user_message_parts.append("- `titulo`: Um título conciso para o post.")
    user_message_parts.append("- `tema`: Resumo do tema abordado no post.")
    user_message_parts.append("- `legenda_principal`: A legenda principal do post.")
    user_message_parts.append("- `variacoes_legenda`: Uma lista de 2-3 variações da legenda principal.")
    user_message_parts.append("- `hashtags`: Uma lista de hashtags relevantes.")
    user_message_parts.append("            \"sugestao_formato\": \"Sugestão de formato para o post (ex: 'Carrossel de imagens', 'Vídeo', 'Reel', 'Imagem única', 'Infográfico'). Pode adicionar explicações.\",")
    user_message_parts.append("- `post_strategy_rationale`: Uma justificativa estratégica detalhada para este post, explicando como ele se encaixa na narrativa semanal e contribui para os objetivos gerais.")
    user_message_parts.append("- `micro_briefing`: Um breve resumo do objetivo e foco principal do post, para contextualização.")
    user_message_parts.append("- `micro_roteiro`: Se `sugestao_formato` for \"Vídeo curto\" ou \"Reel\", inclua um micro-roteiro detalhando cenas, falas/textos e chamadas para ação.")
    user_message_parts.append("- `carrossel_slides`: Se `sugestao_formato` for \"Carrossel de imagens\", inclua uma lista de objetos, onde cada objeto representa um slide do carrossel, contendo `titulo_slide`, `texto_slide` e `sugestao_visual_slide`.")
    user_message_parts.append("- `visual_prompt_suggestion`: Uma descrição detalhada da imagem ou vídeo principal para o post, incluindo estilo, cores, elementos e atmosfera, para ser usada por uma IA de geração de imagens. Evite usar texto no prompt para imagem.")
    user_message_parts.append("- `text_in_image`: Caso tenha alguma sugestão de texto para incluir na imagem. Use este campo.")
    user_message_parts.append("- `visual_description_portuguese`: Uma descrição em português da imagem ou vídeo principal, para ser exibida no briefing.")
    user_message_parts.append("- `cta_individual`: Uma chamada para ação específica para este post.")
    user_message_parts.append("- `interacao`: Sugerir uma pergunta para a audiência ou uma forma de incentivar comentários, aumentando o engajamento além da simples publicação..")
    user_message_parts.append("\n Gere **APENAS UM JSON VÁLIDO**, sem texto adicional, comentários ou explicações. Não inclua marcações de code block (como ```json). Retorne o conteúdo em formato JSON, com a estrutura abaixo:")
    user_message_parts.append("{{")
    user_message_parts.append("    \"weekly_strategy_summary\": \"Resumo da estratégia semanal para a campanha.\",")
    user_message_parts.append("    \"posts\": [")
    user_message_parts.append("        {{")
    user_message_parts.append("            \"titulo\": \"Título do Post 1\",")
    user_message_parts.append("            \"tema\": \"Resumo do tema abordado no post 1\",")
    user_message_parts.append("            \"legenda_principal\": \"Legenda principal do post 1.\",")
    user_message_parts.append("            \"variacoes_legenda\": [")
    user_message_parts.append("                \"Variação 1 da legenda 1.\",")
    user_message_parts.append("                \"Variação 2 da legenda 1.\"")
    user_message_parts.append("            ],")
    user_message_parts.append("            \"hashtags\": [\"#Hashtag1\", \"#Hashtag2\"],")
    user_message_parts.append("            \"horario_de_postagem\": \"Horário sugerido para postagem\",")
    user_message_parts.append("            \"sugestao_formato\": \"Carrossel de imagens\",")
    user_message_parts.append("            \"post_strategy_rationale\": \"Justificativa estratégica para este post.\",")
    user_message_parts.append("            \"micro_briefing\": \"Breve resumo do objetivo do post.\",")
    user_message_parts.append("            \"visual_prompt_suggestion\": \"Descrição detalhada para IA de geração de imagens. Evite usar texto no prompt para imagem\",")
    user_message_parts.append("            \"text_in_image\": \"Caso tenha sugestão de texto para ser incluído na imagem.\",")
    user_message_parts.append("            \"visual_description_portuguese\": \"Descrição em português da imagem ou vídeo principal.\",")
    user_message_parts.append("            \"cta_individual\": \"Chamada para ação específica para este post.\",")
    user_message_parts.append("            \"interacao\": \"Formas de como aumentar a interação com este post.\",")
    user_message_parts.append("            \"micro_roteiro\": [")
    user_message_parts.append("                {")
    user_message_parts.append("                    \"cena\": 1,")
    user_message_parts.append("                    \"descricao\": \"Pessoa sorrindo\",")
    user_message_parts.append("                    \"texto_tela\": \"Problema resolvido!\",")
    user_message_parts.append("                    \"fala\": \"Você sabia que...?\"")
    user_message_parts.append("                }")
    user_message_parts.append("            ],")
    user_message_parts.append("            \"carrossel_slides\": [")
    user_message_parts.append("                {")
    user_message_parts.append("                    \"titulo_slide\": \"Título do Slide 1\",")
    user_message_parts.append("                    \"texto_slide\": \"Texto do slide 1\",")
    user_message_parts.append("                    \"sugestao_visual_slide\": \"Visual para slide 1\"")
    user_message_parts.append("                }")
    user_message_parts.append("            ]")
    user_message_parts.append("        }}")
    user_message_parts.append("    ],")
    user_message_parts.append("    \"metricas_de_sucesso_sugeridas\": " + json.dumps(sugerir_metricas, indent=4, ensure_ascii=False).replace("\n", "\n    ") + ",")
    user_message_parts.append("}}")

    user_message = "\n".join(user_message_parts)

    return f"{system_message}\n\n{user_message}"
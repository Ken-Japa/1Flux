from reportlab.platypus import Paragraph, Spacer

def _build_post_section(styles: dict, post: dict, post_number: int) -> list:
    """
    Constrói a seção de um post individual no PDF.

    Args:
        styles (dict): Dicionário de estilos do ReportLab.
        post (dict): Dicionário com os dados de um post.
        post_number (int): Número do post.

    Returns:
        list: Uma lista de elementos Story para a seção do post.
    """
    post_story = []
    post_story.append(Paragraph(f"Post {post_number}: {post.get('titulo', 'N/A')}", styles['PostTitle']))
    post_story.append(Spacer(1, 7.2))
    post_story.append(Paragraph("Tema:", styles['BlackSubtitle']))
    post_story.append(Spacer(1, 3.6))
    post_story.append(Paragraph(f"{post.get('tema')}", styles['NormalText']))
    post_story.append(Spacer(1, 7.2))

    post_story.append(Paragraph("Justificativa Estratégica:", styles['BlackSubtitle']))
    post_story.append(Spacer(1, 3.6))
    post_story.append(Paragraph(post.get('post_strategy_rationale', 'N/A'), styles['PostContent']))
    post_story.append(Spacer(1, 7.2))

    post_story.append(Paragraph("Briefing:", styles['BlackSubtitle']))
    post_story.append(Spacer(1, 3.6))
    post_story.append(Paragraph(post.get('micro_briefing', 'N/A'), styles['PostContent']))
    post_story.append(Spacer(1, 7.2))
    
    post_story.append(Paragraph("Legenda Principal:", styles['PurpleSubtitle']))
    post_story.append(Spacer(1, 3.6))
    post_story.append(Paragraph(post.get('legenda_principal', 'N/A'), styles['PostContent']))
    post_story.append(Spacer(1, 7.2))

    post_story.append(Paragraph("Variações de Legenda:", styles['StrongPurpleSubtitle']))
    post_story.append(Spacer(1, 3.6))
    for i, variation in enumerate(post.get('variacoes_legenda', [])):
        post_story.append(Paragraph(f"{i+1}. {variation}", styles['PostContent']))
        if i < len(post.get('variacoes_legenda', [])) - 1:
            post_story.append(Spacer(1, 3.6)) # Espaço menor entre as variações
    post_story.append(Spacer(1, 7.2))

    post_story.append(Paragraph("Hashtags:", styles['BlackSubtitle']))
    post_story.append(Spacer(1, 3.6))
    post_story.append(Paragraph(" ".join(post.get('hashtags', [])), styles['PostHashtag']))
    post_story.append(Spacer(1, 7.2))

    # Adiciona indicador_principal
    indicador_principal = post.get('indicador_principal', '')
    if indicador_principal:
        post_story.append(Paragraph("Indicador Principal:", styles['BlackSubtitle']))
        post_story.append(Spacer(1, 3.6))
        post_story.append(Paragraph(indicador_principal, styles['PostContent']))
        post_story.append(Spacer(1, 7.2))
        
    
    post_story.append(Paragraph("Chamada para Ação Individual:", styles['BlackSubtitle']))
    post_story.append(Spacer(1, 3.6))
    post_story.append(Paragraph(post.get('cta_individual'), styles['PostContent']))
    post_story.append(Spacer(1, 7.2))

    # Adiciona o campo de interação
    if post.get('interacao'):
        post_story.append(Paragraph("Sugestões de Interação/Engajamento:", styles['BlackSubtitle']))
        post_story.append(Spacer(1, 3.6))
        post_story.append(Paragraph(post.get('interacao'), styles['PostContent']))
        post_story.append(Spacer(1, 7.2))
    
        # Adiciona o response_script
    response_script = post.get('response_script', [])
    if response_script:
        post_story.append(Paragraph("Roteiro de Respostas:", styles['StrongPurpleSubtitle']))
        post_story.append(Spacer(1, 3.6))
        for script_item in response_script:
            post_story.append(Paragraph(f"<b>Comentário Genérico:</b> {script_item.get('comentario_generico', 'N/A')}", styles['PostContent']))
            post_story.append(Paragraph(f"<b>Resposta Sugerida:</b> {script_item.get('resposta_sugerida', 'N/A')}", styles['PostContent']))
            post_story.append(Paragraph(f"<b>Comentário Negativo:</b> {script_item.get('comentario_negativo', 'N/A')}", styles['PostContent']))
            post_story.append(Paragraph(f"<b>Resposta para Negativo:</b> {script_item.get('resposta_negativo', 'N/A')}", styles['PostContent']))
            post_story.append(Spacer(1, 7.2))
        post_story.append(Spacer(1, 14.4))
        
    # Adiciona a descrição em português da imagem
    visual_description = post.get('visual_description_portuguese', '')
    if visual_description and visual_description != 'N/A':
        post_story.append(Paragraph("Descrição da Imagem:", styles['BlackSubtitle']))
        post_story.append(Spacer(1, 3.6))
        post_story.append(Paragraph(visual_description, styles['PostContent']))
        post_story.append(Spacer(1, 7.2))

    # Adiciona o campo text_in_image
    text_in_image = post.get('text_in_image', '') or ''
    if text_in_image:
        post_story.append(Paragraph("Texto na Imagem/Vídeo:", styles['BlackSubtitle']))
        post_story.append(Spacer(1, 3.6))
        post_story.append(Paragraph(text_in_image, styles['PostContent']))
        post_story.append(Spacer(1, 7.2))
                
    post_story.append(Paragraph("Sugestão de Formato:", styles['DarkGreenSubtitle']))
    post_story.append(Spacer(1, 3.6))
    post_story.append(Paragraph(post.get('sugestao_formato', 'N/A'), styles['PostContent']))
    post_story.append(Spacer(1, 7.2))

    # Adiciona detalhes específicos do formato, se existirem
    sugestao_formato = post.get('sugestao_formato', '')
    if "Carrossel" in sugestao_formato:
        carrossel_slides = post.get('carrossel_slides', [])
        if carrossel_slides:
            post_story.append(Paragraph("Slides do Carrossel:", styles['StrongPurpleSubtitle']))
            post_story.append(Spacer(1, 3.6))
            for i, slide in enumerate(carrossel_slides):
                post_story.append(Paragraph(f"<b>Slide {i+1}:</b> {slide.get('titulo_slide', 'N/A')}", styles['PostContent']))
                post_story.append(Paragraph(f"   <b>Texto:</b> {slide.get('texto_slide', 'N/A')}", styles['PostContent']))
                post_story.append(Paragraph(f"   Visual: {slide.get('sugestao_visual_slide', 'N/A')}", styles['PostContent']))
                post_story.append(Spacer(1, 3.6))
            post_story.append(Spacer(1, 7.2))
    elif "Vídeo" in sugestao_formato or "Reel" in sugestao_formato:
        micro_roteiro = post.get('micro_roteiro', [])
        if micro_roteiro:
            post_story.append(Paragraph("Micro Roteiro:", styles['StrongPurpleSubtitle']))
            post_story.append(Spacer(1, 3.6))
            for i, cena in enumerate(micro_roteiro):
                post_story.append(Paragraph(f"<b>Cena {cena.get('cena', i+1)}:</b> {cena.get('descricao', 'N/A')}", styles['PostContent']))
                post_story.append(Paragraph(f"   <b>Texto na Tela:</b> {cena.get('texto_tela', 'N/A')}", styles['PostContent']))
                post_story.append(Spacer(1, 3.6))
            post_story.append(Spacer(1, 7.2))


    # Adiciona o título para o prompt da IA
    post_story.append(Paragraph("Prompt para IA Geradora de Imagens:", styles['StrongPurpleSubtitle']))
    post_story.append(Spacer(1, 3.6))
    visual_prompt_suggestion = post.get('visual_prompt_suggestion')
    if visual_prompt_suggestion is None:
        visual_prompt_suggestion = ''
    post_story.append(Paragraph(visual_prompt_suggestion, styles['PostContent']))
    post_story.append(Spacer(1, 14.4))

    # Adiciona ab_test_suggestions
    ab_test_suggestions = post.get('ab_test_suggestions', '')
    if ab_test_suggestions:
        post_story.append(Paragraph("Testes A/B:", styles['BlackSubtitle']))
        post_story.append(Spacer(1, 3.6))
        post_story.append(Paragraph(ab_test_suggestions, styles['PostContent']))
        post_story.append(Spacer(1, 7.2))


    # Adiciona optimization_triggers
    optimization_triggers = post.get('optimization_triggers', '')
    if optimization_triggers:
        post_story.append(Paragraph("Como Corrigir a Rota (Gatilhos de Otimização):", styles['BlackSubtitle']))
        post_story.append(Spacer(1, 3.6))
        post_story.append(Paragraph(optimization_triggers, styles['PostContent']))
        post_story.append(Spacer(1, 14.4))

    return post_story
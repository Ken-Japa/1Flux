from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from .styles.pdf_styles import get_table_style_for_gradient_row

# Cores para os posts (exemplo, pode ser expandido)
POST_COLORS = {
    1: {'strong': colors.HexColor('#1A237E')}, # Azul escuro
    2: {'strong': colors.HexColor('#B71C1C')}, # Vermelho escuro
    3: {'strong': colors.HexColor('#004D40')}, # Verde escuro
    4: {'strong': colors.HexColor('#E65100')}, # Laranja escuro
    5: {'strong': colors.HexColor('#4A148C')}, # Roxo escuro
    6: {'strong': colors.HexColor('#212121')}, # Cinza escuro
    7: {'strong': colors.HexColor('#880E4F')}, # Rosa escuro
    8: {'strong': colors.HexColor('#33691E')}, # Verde oliva
    9: {'strong': colors.HexColor('#F57F17')}, # Amarelo escuro
    10: {'strong': colors.HexColor('#0D47A1')}, # Azul muito escuro
}

def _build_post_section(styles: dict, post: dict, post_number: int) -> list:
    """
    Constrói a seção de um post individual no PDF, encapsulando-o em um bloco com estilo.

    Args:
        styles (dict): Dicionário de estilos do ReportLab.
        post (dict): Dicionário com os dados de um post.
        post_number (int): Número do post.

    Returns:
        list: Uma lista de elementos Story contendo a seção do post estilizada.
    """
    # Cria uma lista de elementos para o conteúdo do post
    post_elements = []
    # Use color por post
    post_style = ParagraphStyle(name=f'Post{post_number}', parent=styles['PostTitle'], textColor=POST_COLORS.get(post_number, {'strong': colors.HexColor('#000')})['strong'])
    post_elements.append([Paragraph(f"Post {post_number}: {post.get('titulo', 'N/A')}", post_style)])
    post_elements.append([Spacer(1, 7.2)])

    post_elements.append([Paragraph("Tema:", styles['PostSubtitle'])])
    post_elements.append([Paragraph(f"{post.get('tema')}", styles['NormalText'])])
    post_elements.append([Spacer(1, 0)])

    # Adiciona o horário de postagem
    horario_de_postagem = post.get('horario_de_postagem', '')
    if horario_de_postagem:
        post_elements.append([Paragraph("Horário de Postagem:", styles['PostSubtitle'])])
        post_elements.append([Paragraph(horario_de_postagem, styles['PostContent'])])
        post_elements.append([Spacer(1, 0)])

    post_elements.append([Paragraph("Justificativa Estratégica:", styles['PostSubtitle'])])
    post_elements.append([Paragraph(post.get('post_strategy_rationale', 'N/A'), styles['PostContent'])])
    post_elements.append([Spacer(1, 0)])

    post_elements.append([Paragraph("Briefing:", styles['PostSubtitle'])])
    post_elements.append([Paragraph(post.get('micro_briefing', 'N/A'), styles['PostContent'])])
    post_elements.append([Spacer(1, 0)])
    
    post_elements.append([Paragraph("Legenda Principal:", styles['PostSubtitle'])])
    post_elements.append([Paragraph(post.get('legenda_principal', 'N/A'), styles['PostContent'])])
    post_elements.append([Spacer(1, 0)])

    post_elements.append([Paragraph("Variações de Legenda:", styles['PostSubtitle'])])
    for i, variation in enumerate(post.get('variacoes_legenda', [])):
        post_elements.append([Paragraph(f"{i+1}. {variation}", styles['PostContent'])])
        if i < len(post.get('variacoes_legenda', [])) - 1:
            post_elements.append([Spacer(1, 0)]) # Espaço menor entre as variações
    post_elements.append([Spacer(1, 0)])

    post_elements.append([Paragraph("Hashtags:", styles['PostSubtitle'])])
    post_elements.append([Paragraph(" ".join(post.get('hashtags', [])), styles['PostHashtag'])])
    post_elements.append([Spacer(1, 0)])

    # Adiciona indicador_principal
    indicador_principal = post.get('indicador_principal', '')
    if indicador_principal:
        post_elements.append([Paragraph("Indicador Principal:", styles['PostSubtitle'])])
        post_elements.append([Paragraph(indicador_principal, styles['PostContent'])])
        post_elements.append([Spacer(1, 0)])
        
    
    post_elements.append([Paragraph("Chamada para Ação Individual:", styles['PostSubtitle'])])
    post_elements.append([Paragraph(post.get('cta_individual'), styles['PostContent'])])
    post_elements.append([Spacer(1, 0)])

    # Adiciona o campo de interação
    if post.get('interacao'):
        post_elements.append([Paragraph("Sugestões de Interação/Engajamento:", styles['PostSubtitle'])])
        post_elements.append([Paragraph(post.get('interacao'), styles['PostContent'])])
        post_elements.append([Spacer(1, 0)])
    
        # Adiciona o response_script
    response_script = post.get('response_script', [])
    if response_script:
        post_elements.append([Paragraph("Roteiro de Respostas:", styles['PostSubtitle'])])
        for script_item in response_script:
            post_elements.append([Paragraph(f"<b>Comentário Genérico:</b> {script_item.get('comentario_generico', 'N/A')}", styles['PostContent'])])
            post_elements.append([Paragraph(f"<b>Resposta Sugerida:</b> {script_item.get('resposta_sugerida', 'N/A')}", styles['PostContent'])])
            post_elements.append([Paragraph(f"<b>Comentário Negativo:</b> {script_item.get('comentario_negativo', 'N/A')}", styles['PostContent'])])
            post_elements.append([Paragraph(f"<b>Resposta para Negativo:</b> {script_item.get('resposta_negativo', 'N/A')}", styles['PostContent'])])
            post_elements.append([Spacer(1, 3.6)])
        
    # Adiciona a descrição em português da imagem
    visual_description = post.get('visual_description_portuguese', '')
    if visual_description and visual_description != 'N/A':
        post_elements.append([Paragraph("Descrição da Imagem:", styles['PostSubtitle'])])
        post_elements.append([Paragraph(visual_description, styles['PostContent'])])
        post_elements.append([Spacer(1, 0)])

    # Adiciona o campo text_in_image
    text_in_image = post.get('text_in_image', '') or ''
    if text_in_image:
        post_elements.append([Paragraph("Texto na Imagem/Vídeo:", styles['PostSubtitle'])])
        post_elements.append([Paragraph(text_in_image, styles['PostContent'])])
        post_elements.append([Spacer(1, 0)])
                
    post_elements.append([Paragraph("Sugestão de Formato:", styles['PostSubtitle'])])
    post_elements.append([Paragraph(post.get('sugestao_formato', 'N/A'), styles['PostContent'])])
    post_elements.append([Spacer(1, 0)])

    # Adiciona detalhes específicos do formato, se existirem
    sugestao_formato = post.get('sugestao_formato', '')
    if "Carrossel" in sugestao_formato:
        carrossel_slides = post.get('carrossel_slides', [])
        if carrossel_slides:
            post_elements.append([Paragraph("Slides do Carrossel:", styles['PostSubtitle'])])
            for i, slide in enumerate(carrossel_slides):
                post_elements.append([Paragraph(f"<b>Slide {i+1}:</b> {slide.get('titulo_slide', 'N/A')}", styles['PostContent'])])
                post_elements.append([Paragraph(f"   <b>Texto:</b> {slide.get('texto_slide', 'N/A')}", styles['PostContent'])])
                post_elements.append([Paragraph(f"   Visual: {slide.get('sugestao_visual_slide', 'N/A')}", styles['PostContent'])])
                post_elements.append([Spacer(1, 2.6)])
            post_elements.append([Spacer(1, 1)])
    elif "Vídeo" in sugestao_formato or "Reel" in sugestao_formato:
        micro_roteiro = post.get('micro_roteiro', [])
        if micro_roteiro:
            post_elements.append([Paragraph("Micro Roteiro:", styles['PostSubtitle'])])
            for i, cena in enumerate(micro_roteiro):
                post_elements.append([Paragraph(f"<b>Cena {cena.get('cena', i+1)}:</b> {cena.get('descricao', 'N/A')}", styles['PostContent'])])
                post_elements.append([Paragraph(f"   <b>Texto na Tela:</b> {cena.get('texto_tela', 'N/A')}", styles['PostContent'])])
                post_elements.append([Spacer(1, 2.6)])
            post_elements.append([Spacer(1, 1)])


    # Adiciona o título para o prompt da IA
    post_elements.append([Paragraph("Prompt para IA Geradora de Imagens:", styles['PostSubtitle'])])
    visual_prompt_suggestion = post.get('visual_prompt_suggestion')
    if visual_prompt_suggestion is None:
        visual_prompt_suggestion = ''
    post_elements.append([Paragraph(visual_prompt_suggestion, styles['PostContent'])])
    post_elements.append([Spacer(1, 0)])

    # Adiciona ab_test_suggestions
    ab_test_suggestions = post.get('ab_test_suggestions', '')
    if ab_test_suggestions:
        post_elements.append([Paragraph("Testes A/B:", styles['PostSubtitle'])])
        post_elements.append([Paragraph(ab_test_suggestions, styles['PostContent'])])
        post_elements.append([Spacer(1, 0)])


    # Adiciona optimization_triggers
    optimization_triggers = post.get('optimization_triggers', '')
    if optimization_triggers:
        post_elements.append([Paragraph("Como Corrigir a Rota (Gatilhos de Otimização):", styles['PostSubtitle'])])
        post_elements.append([Paragraph(optimization_triggers, styles['PostContent'])])
        post_elements.append([Spacer(1, 0)])

    # Cria a tabela com o conteúdo do post e aplica o estilo de gradiente
    post_table = Table(post_elements, colWidths=[7.0 * inch])
    
    # Obtém os comandos do estilo de gradiente
    gradient_style_commands = get_table_style_for_gradient_row()._cmds

    new_commands = [
        ('ROUNDEDCORNERS', (0, 0), (-1, -1), [10, 10, 10, 10]),  # Cantos arredondados
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]

    # Combina todos os comandos em uma única lista
    combined_commands = gradient_style_commands + new_commands

    # Aplica o estilo combinado à tabela
    post_table.setStyle(TableStyle(combined_commands))

    return [post_table]
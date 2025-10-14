import json
from reportlab.platypus import Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import black

def _format_future_strategy(strategy_data):
    """
    Formata os dados da estratégia futura (dicionário) em uma string legível para o PDF.
    """
    formatted_text = []
    if isinstance(strategy_data, dict):
        if "posts_nutricao" in strategy_data:
            formatted_text.append("<b>Posts de Nutrição:</b>")
            for post in strategy_data["posts_nutricao"]:
                formatted_text.append(f"- <b>Tema:</b> {post.get("tema", "N/A")}")
                formatted_text.append(f"  <b>Formato:</b> {post.get("formato", "N/A")}")
                formatted_text.append(f"  <b>Objetivo:</b> {post.get("objetivo", "N/A")}")
        if "remarketing" in strategy_data:
            formatted_text.append("<br/><b>Remarketing:</b>")
            for item in strategy_data["remarketing"]:
                formatted_text.append(f"- <b>Estratégia:</b> {item.get("estrategia", "N/A")}")
                formatted_text.append(f"  <b>Canal:</b> {item.get("canal", "N/A")}")
        if "long_term" in strategy_data:
            formatted_text.append("<br/><b>Longo Prazo:</b>")
            long_term_data = strategy_data["long_term"]
            formatted_text.append(f"- <b>Comunidade:</b> {long_term_data.get("comunidade", "N/A")}")
            formatted_text.append(f"  <b>Parcerias:</b> {long_term_data.get("parcerias", "N/A")}")
    return "<br/>".join(formatted_text) if formatted_text else "N/A"

def _build_executive_summary(styles, weekly_strategy_summary_dict, target_audience, tone_of_voice, marketing_objectives, future_strategy="", market_references=None):
    story = []
    story.append(Paragraph("Sumário Executivo", styles['Title']))
    story.append(Spacer(1, 0.2 * 2.54 * 72)) # 0.2 inch spacer

    # Weekly Strategy Summary
    summary_text = weekly_strategy_summary_dict.get('summary', 'N/A')
    story.append(Paragraph("Visão Geral da Semana:", styles['h2']))
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 0.2 * 2.54 * 72))

    # Future Strategy
    if future_strategy:
        story.append(Paragraph("Sugestões para Depois da Campanha:", styles['h2']))
        if isinstance(future_strategy, dict):
            formatted_future_strategy = _format_future_strategy(future_strategy)
            story.append(Paragraph(formatted_future_strategy, styles['Normal']))
        else:
            story.append(Paragraph(future_strategy, styles['Normal']))
        story.append(Spacer(1, 0.2 * 2.54 * 72))
    
    # Target Audience
    story.append(Paragraph("Público-Alvo:", styles['h2']))
    story.append(Paragraph(target_audience, styles['Normal']))
    story.append(Spacer(1, 0.2 * 2.54 * 72))

    # Tone of Voice
    story.append(Paragraph("Tom de Voz:", styles['h2']))
    story.append(Paragraph(tone_of_voice, styles['Normal']))
    story.append(Spacer(1, 0.2 * 2.54 * 72))

    # Marketing Objectives
    story.append(Paragraph("Objetivos de Marketing:", styles['h2']))
    story.append(Paragraph(marketing_objectives, styles['Normal']))
    story.append(Spacer(1, 0.2 * 2.54 * 72))


    # Market References
    if market_references:
        story.append(Paragraph("Referências de Mercado (Concorrentes/Inspirações):", styles['h2']))
        for reference in market_references:
            story.append(Paragraph(f"<b>Nome/Handle:</b> {reference.get('Nome/Handle', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"<b>Diferenciais:</b> {reference.get('Diferenciais', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"<b>Oportunidades:</b> {reference.get('Oportunidades', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"<b>Posicionamento do Cliente:</b> {reference.get('Posicionamento do Cliente', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 0.1 * 2.54 * 72)) # Small spacer between references
        story.append(Spacer(1, 0.2 * 2.54 * 72))

    return story
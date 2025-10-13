import json
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import black

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
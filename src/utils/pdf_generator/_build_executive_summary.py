from reportlab.platypus import Paragraph, Spacer, NextPageTemplate

def _build_executive_summary(styles: dict, weekly_strategy_summary: dict, target_audience: str, tone_of_voice: str, marketing_objectives: str) -> list:
    """
    Constrói a seção de sumário executivo do PDF.

    Args:
        styles (dict): Dicionário de estilos do ReportLab.
        weekly_strategy_summary (dict): Dicionário com o resumo da estratégia semanal.
        target_audience (str): O público-alvo do briefing.
        tone_of_voice (str): O tom de voz a ser utilizado no briefing.
        marketing_objectives (str): Os objetivos de marketing do briefing.

    Returns:
        list: Uma lista de elementos Story para o sumário executivo.
    """
    summary_story = []
    summary_story.append(NextPageTemplate('NormalPage'))

    summary_story.append(Paragraph("Sumário Executivo", styles['SectionTitle']))
    summary_story.append(Spacer(1, 21.6))

    summary_story.append(Paragraph("Resumo da Estratégia Semanal:", styles['SummaryTitle']))
    summary_story.append(Paragraph(weekly_strategy_summary.get('summary', 'N/A'), styles['SummaryText']))
    summary_story.append(Spacer(1, 14.4))

    summary_story.append(Paragraph("Objetivos:", styles['SummaryTitle']))
    summary_story.append(Paragraph(marketing_objectives if marketing_objectives else "N/A", styles['SummaryText']))
    summary_story.append(Spacer(1, 14.4))

    summary_story.append(Paragraph("Público-Alvo:", styles['SummaryTitle']))
    summary_story.append(Paragraph(target_audience if target_audience else "N/A", styles['SummaryText']))
    summary_story.append(Spacer(1, 14.4))

    summary_story.append(Paragraph("Tom de Voz:", styles['SummaryTitle']))
    summary_story.append(Paragraph(tone_of_voice if tone_of_voice else "N/A", styles['SummaryText']))
    summary_story.append(Spacer(1, 36))

    return summary_story
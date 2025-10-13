from reportlab.platypus import Paragraph, Spacer

def _build_success_metrics(styles, suggested_metrics: dict):
    """
    Constrói a seção de métricas de sucesso sugeridas para o PDF.

    Args:
        styles (dict): Dicionário de estilos do PDF.
        suggested_metrics (dict): Dicionário contendo as métricas sugeridas (indicadores_chave e metricas_secundarias).

    Returns:
        list: Uma lista de elementos ReportLab Flowable para a seção de métricas.
    """
    story = []

    story.append(Paragraph("Métricas de Sucesso Sugeridas", styles['SectionTitle']))
    story.append(Spacer(1, 0.2 * 72)) # 0.2 inch of space

    if suggested_metrics:
        indicadores_chave = suggested_metrics.get('indicadores_chave', [])
        metricas_secundarias = suggested_metrics.get('metricas_secundarias', [])

        if indicadores_chave:
            story.append(Paragraph("Indicadores Chave de Performance (KPIs):", styles['h3']))
            for metric in indicadores_chave:
                story.append(Paragraph(f"• {metric}", styles['Normal']))
            story.append(Spacer(1, 0.1 * 72))

        if metricas_secundarias:
            story.append(Paragraph("Métricas Secundárias:", styles['h3']))
            for metric in metricas_secundarias:
                story.append(Paragraph(f"• {metric}", styles['Normal']))
            story.append(Spacer(1, 0.1 * 72))
    else:
        story.append(Paragraph("Nenhuma métrica de sucesso sugerida disponível.", styles['Normal']))

    return story
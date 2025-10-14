from reportlab.platypus import Paragraph, Spacer
import reportlab.graphics.shapes as shapes
import reportlab.graphics.charts.barcharts as barcharts
from reportlab.lib import colors
from reportlab.lib.units import inch

def _build_success_metrics(styles, suggested_metrics: dict):
    """
    Constrói a seção de métricas de sucesso sugeridas para o PDF.

    Args:
        styles (dict): Dicionário de estilos do ReportLab.
        suggested_metrics (dict): Dicionário contendo as métricas sugeridas (indicadores_chave e metricas_secundarias).

    Returns:
        list: Uma lista de elementos ReportLab Flowable para a seção de métricas.
    """
    story = []

    story.append(Paragraph("Métricas de Sucesso Sugeridas", styles['SectionTitle']))
    story.append(Spacer(1, 0.2*inch))

    if suggested_metrics:
        indicadores_chave = suggested_metrics.get('indicadores_chave', [])
        metricas_secundarias = suggested_metrics.get('metricas_secundarias', [])

        if indicadores_chave:
            story.append(Paragraph("Indicadores Chave de Performance (KPIs):", styles['h3']))
            for metric in indicadores_chave:
                story.append(Paragraph(f"• {metric}", styles['NormalAdjusted']))
                story.append(Spacer(1, 0.1 * 1.54 * 36)) 
            story.append(Spacer(1, 0.1*inch))

        if metricas_secundarias:
            story.append(Paragraph("Métricas Secundárias:", styles['h3']))
            for metric in metricas_secundarias:
                story.append(Paragraph(f"• {metric}", styles['NormalAdjusted']))
                story.append(Spacer(1, 0.1 * 1.54 * 36)) 
            story.append(Spacer(1, 0.1*inch))

    else:
        story.append(Paragraph("Nenhuma métrica de sucesso sugerida disponível.", styles['NormalAdjusted']))

    return story
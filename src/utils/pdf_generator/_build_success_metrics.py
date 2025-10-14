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
                story.append(Paragraph(f"• {metric}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))

        if metricas_secundarias:
            story.append(Paragraph("Métricas Secundárias:", styles['h3']))
            for metric in metricas_secundarias:
                story.append(Paragraph(f"• {metric}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))

        # Conditional BarChart (apenas se lengths variam e >1)
        if len(indicadores_chave) > 1 or len(metricas_secundarias) > 1 and len(indicadores_chave) != len(metricas_secundarias):
            drawing = shapes.Drawing(400, 200)
            bc = barcharts.VerticalBarChart()
            bc.x = 50
            bc.y = 50
            bc.height = 125
            bc.width = 300
            bc.data = [[len(indicadores_chave), len(metricas_secundarias)]]
            bc.categoryAxis.labels.angle = 30
            bc.categoryAxis.categoryNames = ['KPIs', 'Secundárias']
            bc.bars[0].fillColor = colors.HexColor('#1A237E')
            drawing.add(bc)
            story.append(drawing)
            story.append(Spacer(1, 0.1*inch))
    else:
        story.append(Paragraph("Nenhuma métrica de sucesso sugerida disponível.", styles['Normal']))

    return story
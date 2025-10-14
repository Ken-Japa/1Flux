from reportlab.platypus import Paragraph, Spacer, NextPageTemplate, PageBreak, Table, TableStyle
import reportlab.graphics.shapes as shapes
import reportlab.graphics.charts.barcharts as barcharts
from reportlab.lib import colors # Importar colors
from reportlab.lib.units import inch

def _build_publication_calendar(styles: dict, publication_calendar: list) -> list:
    """
    Constrói a seção de calendário de publicação do PDF.

    Args:
        styles (dict): Dicionário de estilos do ReportLab.
        publication_calendar (list): Lista de entradas do calendário de publicação.

    Returns:
        list: Uma lista de elementos Story para o calendário de publicação.
    """
    calendar_story = []
    calendar_story.append(Paragraph("Calendário de Publicação Sugerido", styles['SectionTitle']))
    calendar_story.append(Spacer(1, 21.6))
    if not publication_calendar:
        calendar_story.append(Paragraph("Nenhum calendário de publicação sugerido disponível.", styles['NormalText']))
        return calendar_story

    data = [['Dia/Data', 'Horário', 'Post']]
    for day_entry in publication_calendar:
        day = day_entry.get('day', 'N/A')
        for entry in day_entry.get('entries', []):
            time = f"<b>{entry.get('time', 'N/A')}</b>"
            content = f"Post {entry.get('post_number')}: {entry.get('content', 'N/A')}"
            data.append([day, Paragraph(time, styles['NormalText']), Paragraph(content, styles['TableCell'])])
            day = ''

    table = Table(data, colWidths=[2*inch, 1.5*inch, 3*inch])
    ts = [
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A237E')),  # Header
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'DejaVuSans-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#E8EAF6')]),  # Alternating
        ('ROUNDEDCORNERS', [10, 10, 10, 10]),  # Rounded all corners
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#E8EAF6')),
    ]
    table.setStyle(TableStyle(ts))
    calendar_story.append(table)
    calendar_story.append(Spacer(1, 0.2*inch))

    # Conditional chart (apenas se variação em counts)
    post_counts = {day_entry.get('day'): len(day_entry.get('entries', [])) for day_entry in publication_calendar}
    if post_counts and max(post_counts.values()) - min(post_counts.values()) > 0:  # Variação
        drawing = shapes.Drawing(400, 200)
        bc = barcharts.VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 300
        bc.data = [[count for count in post_counts.values()]]
        bc.categoryAxis.labels.angle = 30
        bc.categoryAxis.categoryNames = list(post_counts.keys())
        bc.bars[0].fillColor = colors.HexColor('#1A237E')
        drawing.add(bc)
        calendar_story.append(drawing)
        calendar_story.append(Spacer(1, 0.1*inch))

    return calendar_story
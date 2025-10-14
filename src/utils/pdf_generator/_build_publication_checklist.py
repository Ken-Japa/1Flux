from reportlab.platypus import Paragraph, Spacer, NextPageTemplate, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def _build_publication_checklist(styles: dict, publication_checklist: list) -> list:
    """
    Constrói a seção de checklist de publicação do PDF.

    Args:
        styles (dict): Objeto de estilos do ReportLab.
        publication_checklist (list): Lista de itens do checklist de publicação.

    Returns:
        list: Uma lista de elementos Story para o checklist de publicação.
    """
    checklist_story = []
    checklist_story.append(Paragraph("Checklist de Publicação", styles['SectionTitle']))
    checklist_story.append(Spacer(1, 0.2*inch))

    if not publication_checklist:
        checklist_story.append(Paragraph("Nenhum checklist de publicação disponível.", styles['NormalText']))
        return checklist_story

    data = [['Data', 'Tipo', 'Tarefa']]
    task_order = {"Postar":1,"Preparar":2,"Responder comentários":3,"Responder 2ª vez comentários":4}

    for day_entry in publication_checklist:
        date = day_entry['date']
        sorted_tasks = sorted(day_entry['tasks'], key=lambda x: task_order.get(x['type'],99))
        for task in sorted_tasks:
            type_ = task['type']
            post_num = task['post_number']
            title = task['title']
            task_str = f"{type_} Post {post_num}: '{title}'"
            # Use style for color
            style_name = f'Checklist{type_.split()[0]}_Post{post_num}'  # Adapt
            data.append([date, type_, Paragraph(task_str, styles.get(style_name, 'ChecklistItem'))])
            date = ''

    table = Table(data, colWidths=[1*inch, 1.5*inch, 4*inch])
    ts = [
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3F51B5')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'DejaVuSans-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#E8EAF6')]),
        ('ROUNDEDCORNERS', [10, 10, 10, 10]),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#E8EAF6')),
    ]
    table.setStyle(TableStyle(ts))
    checklist_story.append(table)
    checklist_story.append(Spacer(1, 0.2*inch))

    return checklist_story
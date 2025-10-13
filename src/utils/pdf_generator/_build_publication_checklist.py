from reportlab.platypus import Paragraph, Spacer, NextPageTemplate, PageBreak

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
    checklist_story.append(NextPageTemplate('NormalPage'))
    checklist_story.append(PageBreak())
    checklist_story.append(Paragraph("Checklist de Publicação", styles['SectionTitle']))
    checklist_story.append(Spacer(1, 21.6))

    if not publication_checklist:
        checklist_story.append(Paragraph("Nenhum checklist de publicação disponível.", styles['NormalText']))
        return checklist_story

    for day_entry in publication_checklist:
        checklist_story.append(Paragraph(f"<b>{day_entry['date']}</b>", styles['ChecklistDate']))
        
        # Definir a ordem de prioridade para os tipos de tarefa
        task_order = {"Postar": 1, "Preparar": 2, "Responder comentários": 3, "Responder 2ª vez comentários": 4}
        
        # Ordenar as tarefas com base na prioridade
        sorted_tasks = sorted(day_entry['tasks'], key=lambda x: task_order.get(x['type'], 99))

        for task in sorted_tasks:
            task_type = task['type']
            post_number = task['post_number']
            task_title = task['title']

            if task_type == "Preparar":
                task_type_key = "Preparar"
                formatted_task_title = f"Preparar Post {post_number}: '{task_title}'"
            elif task_type == "Postar":
                task_type_key = "Postar"
                formatted_task_title = f"Postar Post {post_number}: '{task_title}'"
            elif task_type == "Responder comentários":
                task_type_key = "Responder"
                formatted_task_title = f"Responder comentários do Post {post_number}: '{task_title}'"
            elif task_type == "Responder 2ª vez comentários":
                task_type_key = "Responder"
                formatted_task_title = f"Responder 2ª vez comentários do Post {post_number}: '{task_title}'"
            
            style_name = f'Checklist{task_type_key}_Post{post_number}'
            if style_name in styles:
                checklist_story.append(Paragraph(formatted_task_title, styles[style_name]))
            else:
                # Fallback to a generic style if the specific one is not found
                checklist_story.append(Paragraph(formatted_task_title, styles['ChecklistItem']))
        checklist_story.append(Spacer(1, 7.2)) # Espaço após cada dia

    return checklist_story
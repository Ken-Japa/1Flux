from datetime import datetime, timedelta
from collections import defaultdict

def generate_publication_checklist(publication_calendar: list) -> list:
    """
    Gera um checklist de publicação com base no calendário de publicação, agrupado por dia.

    Args:
        publication_calendar (list): O calendário de publicação gerado, contendo dias e posts.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa um dia com suas tarefas.
    """
    daily_checklist = defaultdict(list)
    
    for day_entry in publication_calendar:
        day_name_and_date = day_entry["day"]
        # Extrair a data para cálculo
        day_date_str = day_name_and_date.split(', ')[1] # Ex: "17/10"
        current_year = datetime.now().year
        try:
            day_date = datetime.strptime(f"{day_date_str}/{current_year}", "%d/%m/%Y")
        except ValueError:
            day_date = datetime.now() # Fallback

        for post_entry in day_entry["entries"]:
            post_title = post_entry["content"]
            post_number = post_entry["post_number"]
            
            # Preparar o post: 2 dias antes
            prepare_date = day_date - timedelta(days=2)
            daily_checklist[prepare_date.strftime("%d/%m")].append({"type": "Preparar", "title": post_title, "post_number": post_number})
            
            # Postar (ou agendar): No dia do post
            daily_checklist[day_date.strftime("%d/%m")].append({"type": "Postar", "title": post_title, "post_number": post_number})
            
            # Responder comentários: 2 dias depois
            respond_date_2_days = day_date + timedelta(days=2)
            daily_checklist[respond_date_2_days.strftime("%d/%m")].append({"type": "Responder comentários", "title": post_title, "post_number": post_number})

        # Responder comentários: 4 dias depois
        respond_checklist = day_date + timedelta(days=4)
        daily_checklist[respond_checklist.strftime("%d/%m")].append({"type": "Responder 2ª vez comentários", "title": post_title, "post_number": post_number})

    # Converter o defaultdict para uma lista de dicionários e ordenar por data
    sorted_checklist = []
    for date_str in sorted(daily_checklist.keys(), key=lambda x: datetime.strptime(x, "%d/%m")):
        sorted_checklist.append({"date": date_str, "tasks": daily_checklist[date_str]})

    return sorted_checklist
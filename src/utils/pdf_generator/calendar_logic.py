from datetime import datetime, timedelta
import json
from collections import defaultdict

def generate_publication_calendar(start_date: datetime, posts_list: list) -> list:
    """
    Gera um calendário de publicação sugerido para a próxima semana, distribuindo posts.

    Args:
        start_date (datetime): A data de início para calcular a semana.
        posts_list (list): Uma lista de dicionários, onde cada dicionário representa um post e contém um 'title'.

    Returns:
        list: Uma lista de dicionários representando o calendário de publicação, com posts atribuídos a dias.
    """
    calendar = []
    # Dias da semana priorizados para posts: Sexta (4), Sábado (5), Domingo (6), Segunda (0), Quarta (2)
    # datetime.weekday() retorna 0 para Segunda e 6 para Domingo
    prioritized_days_of_week = [4, 5, 6, 0, 2]
    
    # Encontrar a próxima sexta-feira a partir da start_date
    days_until_next_friday = (4 - start_date.weekday() + 7) % 7
    next_friday = start_date + timedelta(days=days_until_next_friday)

    # Gerar as datas para a semana começando na próxima sexta-feira
    week_dates = {}
    current_day_for_week = next_friday
    for _ in range(7):
        week_dates[current_day_for_week.weekday()] = current_day_for_week
        current_day_for_week += timedelta(days=1)

    posts_to_assign = list(posts_list) # Copia a lista para poder manipular
    assigned_posts_by_day = {day: [] for day in prioritized_days_of_week}

    # Distribuir os posts nos dias prioritários
    post_counter = 1 # Inicializa o contador de posts
    post_index = 0 # Inicializa o índice do post
    day_cycle_index = 0
    while post_index < len(posts_to_assign):
        day_of_week = prioritized_days_of_week[day_cycle_index % len(prioritized_days_of_week)]
        assigned_posts_by_day[day_of_week].append({"post_number": post_counter, "post_data": posts_to_assign[post_index]})
        post_index += 1
        post_counter += 1 # Incrementa o contador de posts
        day_cycle_index += 1

    # Construir o calendário final com as datas corretas
    for day_index in prioritized_days_of_week:
        if day_index in week_dates and assigned_posts_by_day[day_index]:
            date_for_day = week_dates[day_index]
            day_name = date_for_day.strftime("%A, %d/%m").replace("Monday", "Segunda-feira").replace("Tuesday", "Terça-feira").replace("Wednesday", "Quarta-feira").replace("Thursday", "Quinta-feira").replace("Friday", "Sexta-feira").replace("Saturday", "Sábado").replace("Sunday", "Domingo")
            
            entries = []
            for assigned_post in assigned_posts_by_day[day_index]:
                horarios_raw = assigned_post["post_data"].get("horario_de_postagem", "Horário não informado")

                post_time = "Horário não informado"
                if isinstance(horarios_raw, str):
                    # Se for uma string, tenta extrair apenas o horário se houver um dia da semana
                    if "," in horarios_raw:
                        parts = horarios_raw.split(",", 1) # Divide apenas na primeira vírgula
                        if len(parts) > 1:
                            post_time = parts[1].strip() # Pega a parte depois da vírgula e remove espaços
                        else:
                            post_time = horarios_raw.strip() # Se não houver vírgula, usa a string inteira
                    else:
                        post_time = horarios_raw.strip() # Se não houver vírgula, usa a string inteira
                elif isinstance(horarios_raw, dict):
                    # Se for um dicionário, tenta extrair pelo dia da semana
                    day_name_lower = day_name.split(',')[0].lower()
                    if "-feira" in day_name_lower:
                        day_name_key = day_name_lower.replace("-feira", "")
                    else:
                        day_name_key = day_name_lower
                    post_time = horarios_raw.get(day_name_key, "Horário não informado")

                entries.append({"time": post_time, "content": assigned_post["post_data"].get("titulo", "Título não disponível"), "post_number": assigned_post["post_number"]})
            
            calendar.append({"day": day_name, "entries": entries})

    # Ordenar o calendário por data (garantindo o ano para ordenação correta)
    calendar.sort(key=lambda x: datetime.strptime(x["day"].split(', ')[1] + f"/{start_date.year}", "%d/%m/%Y"))

    return calendar
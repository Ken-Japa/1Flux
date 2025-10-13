import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, PageBreak, PageTemplate, Frame
from src.utils.pdf_generator.styles.pdf_styles import get_pdf_styles
from src.utils.pdf_generator._build_cover_page import _build_cover_page
from reportlab.lib.units import inch
from src.utils.pdf_generator._build_executive_summary import _build_executive_summary
from src.utils.pdf_generator._build_post_section import _build_post_section
from src.utils.pdf_generator._build_publication_calendar import _build_publication_calendar
from src.utils.pdf_generator._build_publication_checklist import _build_publication_checklist
from src.utils.pdf_generator._header_footer import _header_footer
from src.utils.pdf_generator.calendar_logic import generate_publication_calendar
from src.utils.pdf_generator.checklist_logic import generate_publication_checklist
from src.utils.pdf_generator._build_success_metrics import _build_success_metrics


def create_briefing_pdf(content_json: dict, client_name: str, output_filename: str, model_name: str = "Unknown", target_audience: str = "", tone_of_voice: str = "", marketing_objectives: str = "", suggested_metrics: dict = {}, posting_time: str = ""):
    """
    Converte o JSON de conteúdo gerado em um "PDF de Briefing Profissional".

    Args:
        content_json (dict): O objeto JSON com os posts, legendas, variações, hashtags e formatos.
        client_name (str): Nome do cliente para personalizar o PDF.
        output_filename (str): Nome do arquivo PDF a ser salvo.
        model_name (str): Nome do modelo de IA que gerou o conteúdo (ex: "Gemini", "Mistral").
        target_audience (str): O público-alvo do briefing.
        tone_of_voice (str): O tom de voz a ser utilizado no briefing.
        marketing_objectives (str): Os objetivos de marketing do briefing.
    """
    # Salvar o content_json bruto em um arquivo para depuração
    current_file_path = os.path.abspath(__file__)
    project_root = current_file_path
    while os.path.basename(project_root) != "plataforma_automacao_ia_generativa":
        project_root = os.path.dirname(project_root)
        if project_root == os.path.dirname(project_root): # Reached filesystem root
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__))) # Fallback
            break

    debug_output_dir = os.path.join(project_root, 'output_files', 'respostas_IA', model_name)
    os.makedirs(debug_output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    debug_file_path = os.path.join(debug_output_dir, f"{model_name}_content_json_debug_{timestamp}.json")
    with open(debug_file_path, 'w', encoding='utf-8') as f:
        json.dump(content_json, f, indent=4, ensure_ascii=False)
    print(f"Content_json salvo para depuração em: {debug_file_path}")

    # Garante que content_json é um dicionário, caso seja passado como string JSON
    if isinstance(content_json, str):
        try:
            content_json = json.loads(content_json)
        except json.JSONDecodeError:
            content_json = {}
    elif not isinstance(content_json, dict):
        content_json = {}

    posts = content_json.get('posts', [])
    if isinstance(posts, str):
        try:
            posts = json.loads(posts)
        except json.JSONDecodeError:
            posts = []
    if not isinstance(posts, list):
        posts = []

    styles = get_pdf_styles()
    story = []
    frame_width = letter[0] - 2 * inch
    frame_height = letter[1] - 2 * inch
    normal_frame = Frame(inch,
                         inch,
                         frame_width,
                         frame_height,
                         id='normal')

    normal_page_template = PageTemplate(id='NormalPage', frames=normal_frame, onPage=_header_footer)

    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    doc.addPageTemplates([normal_page_template])

    today = datetime.now()
    formatted_generation_date = today.strftime('%d/%m/%y')

    # --- Calendário de Publicação ---
    # Gerar o calendário de publicação com base na data atual e na lista de posts
    publication_calendar = generate_publication_calendar(today, posts)

    # Extrair a última data do calendário de publicação para o período final
    latest_date = None
    if publication_calendar:
        for entry in publication_calendar:
            # A data está na string 'day', por exemplo "Sexta-feira, 26/07"
            day_str = entry['day'].split(', ')[1] # Pega "26/07"
            # Adiciona o ano atual para criar um objeto datetime completo
            current_calendar_date = datetime.strptime(f"{day_str}/{today.year}", "%d/%m/%Y")
            if latest_date is None or current_calendar_date > latest_date:
                latest_date = current_calendar_date

    start_date = datetime.now()
    if latest_date:
        # Formata a data para o padrão DD/MM/AA
        formatted_period = f"{start_date.strftime('%d/%m/%y')} a {latest_date.strftime('%d/%m/%y')}"
    else:
        formatted_period = f"{start_date.strftime('%d/%m/%y')}"

    # --- Página de Rosto ---
    story.extend(_build_cover_page(styles, client_name, formatted_period, formatted_generation_date))

    # --- Sumário Executivo / Visão Geral da Semana ---
    story.append(PageBreak()) # Adiciona quebra de página antes do sumário executivo
    weekly_strategy_summary_content = content_json.get('weekly_strategy_summary', '')
    if isinstance(weekly_strategy_summary_content, str):
        # Se for uma string, tenta carregar como JSON. Se falhar, usa a string como summary.
        try:
            weekly_strategy_summary_dict = json.loads(weekly_strategy_summary_content)
        except json.JSONDecodeError:
            weekly_strategy_summary_dict = {'summary': weekly_strategy_summary_content}
    elif isinstance(weekly_strategy_summary_content, dict):
        weekly_strategy_summary_dict = weekly_strategy_summary_content
    else:
        weekly_strategy_summary_dict = {}
    story.extend(_build_executive_summary(styles, weekly_strategy_summary_dict, target_audience, tone_of_voice, marketing_objectives))

    # --- Seção de Posts ---
    story.append(PageBreak()) 
    story.append(Paragraph("Ideias de Conteúdo para a Semana", styles['SectionTitle']))
    story.append(Spacer(1, 36)) 

    for i, post in enumerate(posts):
        # Garante que cada 'post' individual é um dicionário
        if isinstance(post, str):
            try:
                post = json.loads(post)
            except json.JSONDecodeError:
                post = {}
        elif not isinstance(post, dict):
            post = {}
        story.extend(_build_post_section(styles, post, i + 1))
        if i < len(posts) - 1:
            story.append(PageBreak())

    # --- Calendário de Publicação ---
    # Gerar o calendário de publicação com base na data atual e na lista de posts
    story.extend(_build_publication_calendar(styles, publication_calendar))
    
        # --- Métricas de Sucesso Sugeridas ---
    story.append(PageBreak())
    story.extend(_build_success_metrics(styles, suggested_metrics))
    
    # --- Checklist de Publicação ---
    story.append(Spacer(1, 36))

    publication_checklist = generate_publication_checklist(publication_calendar)
    story.extend(_build_publication_checklist(styles, publication_checklist))

    doc.build(story)

    return story
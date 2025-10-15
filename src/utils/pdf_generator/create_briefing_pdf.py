import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, PageTemplate, Frame, NextPageTemplate, KeepTogether, HRFlowable
from src.utils.pdf_generator.styles.pdf_styles import get_pdf_styles
from src.utils.pdf_generator._build_cover_page import _build_cover_page
from reportlab.lib.units import inch
from src.utils.pdf_generator._build_executive_summary import _build_executive_summary
from src.utils.pdf_generator._build_post_section import _build_post_section
import reportlab.graphics.shapes as shapes
import reportlab.graphics.charts.barcharts as barcharts
from reportlab.graphics.charts.piecharts import Pie
from src.utils.pdf_generator._build_publication_calendar import _build_publication_calendar
from src.utils.pdf_generator._build_publication_checklist import _build_publication_checklist
from src.utils.pdf_generator._header_footer import _header_footer
from src.utils.pdf_generator.calendar_logic import generate_publication_calendar
from src.utils.pdf_generator.checklist_logic import generate_publication_checklist
from src.utils.pdf_generator._build_success_metrics import _build_success_metrics
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors # Importar colors
# from reportlab.graphics.renderPDF import LinearGradient # Importar LinearGradient

def _cover_page_background(canvas, doc):
    """
    Desenha o fundo colorido para a página de capa.
    """
    canvas.saveState()
    canvas.linearGradient(0, 0, 0, doc.height, [colors.HexColor('#1A237E'), colors.HexColor('#0D47A1')])
    canvas.restoreState()

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

    debug_output_dir = os.path.join(project_root, '..', '..', '..', 'output_files', 'respostas_IA', model_name)
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
    
    doc = SimpleDocTemplate(output_filename, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=36)
    
    today = datetime.now()
    formatted_generation_date = today.strftime('%d/%m/%y')
    
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
    
    # Templates 
    cover_template = PageTemplate(id='CoverPage', frames=Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='cover'), onPage=_cover_page_background) 
    normal_frame = Frame(doc.leftMargin, doc.bottomMargin + 0.5*inch, doc.width, doc.height - 1.5*inch, id='normal')  # Espaço header 
    normal_template = PageTemplate(id='NormalPage', frames=[normal_frame], onPage=_header_footer) 
    doc.addPageTemplates([cover_template, normal_template]) 

    # Capa 
    story.append(NextPageTemplate('CoverPage')) 
    story.extend(_build_cover_page(styles, client_name, formatted_period, formatted_generation_date)) 
    story.append(NextPageTemplate('NormalPage')) 
    story.append(PageBreak())  # Após capa 

    # --- Sumário Executivo / Visão Geral da Semana ----
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
    future_strategy = content_json.get('future_strategy', '')
    market_references = content_json.get('market_references', None)

    story.extend(_build_executive_summary(
        styles,
        weekly_strategy_summary_dict,
        target_audience,
        tone_of_voice,
        marketing_objectives,
        future_strategy=future_strategy,
        market_references=market_references
    ))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#3F51B5'), spaceBefore=12, spaceAfter=12))

        # --- Calendário de Publicação ---
    story.append(PageBreak())
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#3F51B5'), spaceBefore=12))
    # Gerar o calendário de publicação com base na data atual e na lista de posts
    start_date_str = content_json.get('start_date')
    if start_date_str:
        try:
            start_date_for_calendar = datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            start_date_for_calendar = datetime.now()
    else:
        start_date_for_calendar = datetime.now()

    publication_calendar = generate_publication_calendar(start_date_for_calendar, posts)
    story.extend(_build_publication_calendar(styles, publication_calendar))
    
    # --- Seção de Posts ---
    story.append(PageBreak())

    for i, post in enumerate(posts):
        # Garante que cada 'post' individual é um dicionário
        if isinstance(post, str):
            try:
                post = json.loads(post)
            except json.JSONDecodeError:
                post = {}
        elif not isinstance(post, dict):
            post = {}
        
        post_content = _build_post_section(styles, post, i + 1)
        story.append(KeepTogether(post_content))
        story.append(Spacer(1, 0.3*inch))
        if i < len(posts):
            story.append(HRFlowable(width="80%", thickness=0.5, color=colors.grey, hAlign='CENTER', spaceAfter=12))

    story.append(PageBreak())
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#3F51B5'), spaceBefore=12))
    story.extend(_build_success_metrics(styles, suggested_metrics))
    story.append(Spacer(1, 20))
    
    
    # --- Checklist de Publicação ---
    story.append(PageBreak())
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#3F51B5'), spaceBefore=12))
    publication_checklist = generate_publication_checklist(publication_calendar)
    story.extend(_build_publication_checklist(styles, publication_checklist))

    doc.build(story)

    return story


def register_fonts():
    """
    Registra as fontes DejaVu Sans para uso no ReportLab.
    Isso permite a renderização correta de caracteres Unicode, incluindo emojis.
    """
    try:
        # 1. Registra as fontes
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'src/utils/pdf_generator/styles/fonts/dejavu-sans.book.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'src/utils/pdf_generator/styles/fonts/dejavu-sans.bold.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Oblique', 'src/utils/pdf_generator/styles/fonts/dejavu-sans.oblique.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-BoldOblique', 'src/utils/pdf_generator/styles/fonts/dejavu-sans.bold-oblique.ttf'))

        # 2. Cria um alias para facilitar o uso
        pdfmetrics.registerFontFamily('DejaVuSans',
                                      normal='DejaVuSans',
                                      bold='DejaVuSans-Bold',
                                      italic='DejaVuSans-Oblique',
                                      boldItalic='DejaVuSans-BoldOblique')
        print("Fontes DejaVu Sans registradas com sucesso.")
    except Exception as e:
        print(f"Erro ao registrar fontes: {e}")

register_fonts()
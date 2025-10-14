import os
from datetime import datetime
from reportlab.platypus import Paragraph, Spacer, Image
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.styles import ParagraphStyle

from reportlab.lib.colors import HexColor

from src.config import COMPANY_NAME, LOGO_PATH

def _build_cover_page(styles: dict, client_name: str, formatted_period: str, formatted_generation_date: str) -> list:
    """
    Constrói a página de capa do PDF.

    Args:
        styles (dict): Dicionário de estilos do ReportLab.
        client_name (str): Nome do cliente para personalizar o PDF.
        formatted_period (str): O período completo do briefing, já formatado (ex: "Período 06/10/25 a 15/10/25").
        formatted_generation_date (str): A data de geração do PDF, já formatada (ex: "06/10/25").

    Returns:
        list: Uma lista de elementos Story para a capa.
    """
    cover_story = []

    # Definir estilos para a capa com texto branco
    cover_title_style = ParagraphStyle(name='CoverTitle', parent=styles['TitleStyle'], textColor=HexColor('#FFFFFF'), alignment=1)
    cover_subtitle_style = ParagraphStyle(name='CoverSubtitle', parent=styles['SubtitleStyle'], textColor=HexColor('#FFFFFF'), alignment=1)

    cover_story.append(Spacer(1, 150)) # Espaçamento maior no topo
    cover_story.append(Paragraph(f"Calendário Semanal de Conteúdo", cover_title_style))
    cover_story.append(Paragraph(f"para {client_name}", cover_subtitle_style))
    cover_story.append(Spacer(1, 24)) # Espaçamento ajustado
    cover_story.append(Paragraph(formatted_period, cover_subtitle_style))
    cover_story.append(Spacer(1, 48)) # Espaçamento ajustado
    cover_story.append(Paragraph(COMPANY_NAME, cover_subtitle_style))

    
    # Inserir Logo
    if os.path.exists(LOGO_PATH):
        try:
            logo = Image(LOGO_PATH)
            # Ajusta o tamanho do logo para caber na página, mantendo a proporção
            logo_width = 250  # Aumenta o tamanho do logo
            logo_height = logo.drawHeight * (logo_width / logo.drawWidth)
            logo.drawWidth = logo_width
            logo.drawHeight = logo_height
            logo.hAlign = 'CENTER'
            cover_story.append(logo)
            cover_story.append(Spacer(1, 48)) # Espaçamento ajustado
        except Exception as e:
            print(f"Erro ao carregar o logo: {e}")
            cover_story.append(Paragraph("[ERRO AO CARREGAR LOGO]", cover_subtitle_style))
    else:
        cover_story.append(Paragraph("[LOGO NÃO ENCONTRADO]", cover_subtitle_style))
    cover_story.append(Spacer(1, 48)) # Espaçamento ajustado
    cover_story.append(Paragraph(f"Gerado em: {formatted_generation_date}", cover_subtitle_style))
    return cover_story
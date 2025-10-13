from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

from src.config import COMPANY_NAME

def _header_footer(canvas_obj: canvas.Canvas, doc) -> None:
    """
    Adiciona cabeçalho e rodapé a cada página do PDF.

    Args:
        canvas_obj (canvas.Canvas): O objeto canvas do ReportLab.
        doc: O objeto documento do ReportLab.
    """
    canvas_obj.saveState()
    # Rodapé
    footer_text = f"{COMPANY_NAME} | Página {doc.page}"
    canvas_obj.setFont('Helvetica', 9)
    canvas_obj.setFillColor(HexColor('#757575'))
    canvas_obj.drawCentredString(letter[0] / 2.0, 54, footer_text)
    canvas_obj.restoreState()
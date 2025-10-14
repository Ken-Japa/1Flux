from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
import os

from src.config import COMPANY_NAME, LOGO_PATH

def _header_footer(canvas_obj: canvas.Canvas, doc) -> None:
    """
    Adiciona cabeçalho e rodapé a cada página do PDF.

    Args:
        canvas_obj (canvas.Canvas): O objeto canvas do ReportLab.
        doc: O objeto documento do ReportLab.
    """
    canvas_obj.saveState()

    # Header Logo 
    if os.path.exists(LOGO_PATH): 
        canvas_obj.drawImage(LOGO_PATH, doc.leftMargin, doc.height + doc.topMargin - inch, width=inch, height=0.5*inch, preserveAspectRatio=True, mask='auto') 
    
    # Footer 
    footer_text = f"{COMPANY_NAME} | Página {doc.page}" 
    canvas_obj.setFont('DejaVuSans', 9) 
    canvas_obj.setFillColor(HexColor('#757575')) 
    canvas_obj.drawCentredString(doc.width / 2.0 + doc.leftMargin, doc.bottomMargin / 2, footer_text) 
    
    canvas_obj.restoreState()
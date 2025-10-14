from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib import colors

def get_pdf_styles():
    styles = getSampleStyleSheet()

    # --- Estilos Personalizados ---
    # Título Principal
    styles.add(ParagraphStyle(name='FooterStyle', 
                               fontSize=9, 
                               leading=10, 
                               alignment=TA_CENTER, 
                               fontName='DejaVuSans',
                               textColor=HexColor('#757575'))) # Cinza médio

    # Título Principal
    styles.add(ParagraphStyle(name='TitleStyle', 
                               fontSize=24, 
                               leading=28, 
                               alignment=TA_CENTER, 
                               spaceAfter=0,
                               fontName='DejaVuSans-Bold',
                               textColor=HexColor('#1A237E'))) # Azul escuro
    # Subtítulo
    styles.add(ParagraphStyle(name='SubtitleStyle', 
                               fontSize=18, 
                               leading=22, 
                               alignment=TA_CENTER, 
                               spaceAfter=0,
                               fontName='DejaVuSans',
                               textColor=HexColor('#3F51B5'))) # Azul médio

    # Estilos para o Checklist de Publicação com cores por post e tipo de tarefa
    # Cores base para os posts
    POST_COLORS = {
        1: {"strong": HexColor('#1A237E'), "medium": HexColor('#5C6BC0'), "light": HexColor('#9FA8DA')}, # Azul
        2: {"strong": HexColor('#2E7D32'), "medium": HexColor('#66BB6A'), "light": HexColor('#A5D6A7')}, # Verde
        3: {"strong": HexColor('#EF6C00'), "medium": HexColor('#FFA726'), "light": HexColor('#FFCC80')}, # Laranja
        4: {"strong": HexColor('#4A148C'), "medium": HexColor('#9575CD'), "light": HexColor('#B39DDB')}, # Roxo
        5: {"strong": HexColor('#B71C1C'), "medium": HexColor('#E57373'), "light": HexColor('#EF9A9A')}  # Vermelho
    }

    # Adicionar estilos para cada tipo de tarefa e post
    for i in range(1, 6):
        # Estilo para Postar (cor forte)
        styles.add(ParagraphStyle(name=f'ChecklistPostar_Post{i}',
                                   fontSize=10,
                                   leading=12,
                                   spaceBefore=0,
                                   spaceAfter=0,
                                   fontName='DejaVuSans-Bold',
                                   textColor=POST_COLORS[i]["strong"]))
        # Estilo para Preparar (cor média)
        styles.add(ParagraphStyle(name=f'ChecklistPreparar_Post{i}',
                                   fontSize=10,
                                   leading=12,
                                   spaceBefore=1,
                                   spaceAfter=1,
                                   fontName='DejaVuSans',
                                   textColor=POST_COLORS[i]["medium"]))
        # Estilo para Responder (cor clara)
        styles.add(ParagraphStyle(name=f'ChecklistResponder_Post{i}',
                                   fontSize=10,
                                   leading=12,
                                   spaceBefore=1,
                                   spaceAfter=1,
                                   fontName='DejaVuSans-Oblique',
                                   textColor=POST_COLORS[i]["light"]))



    styles.add(ParagraphStyle(name='SectionTitle', fontSize=18, leading=22, textColor=HexColor('#1A237E'), spaceAfter=12))
    # Texto Normal
    styles.add(ParagraphStyle(name='NormalText', 
                           fontSize=11, 
                           leading=14, 
                           spaceAfter=0,
                           fontName='DejaVuSans',
                           textColor=HexColor('#212121'))) # Quase preto

    # Hashtags
    styles.add(ParagraphStyle(name='HashtagStyle', 
                           fontSize=11, 
                           leading=14, 
                           spaceAfter=0,
                           fontName='DejaVuSans-Bold',
                           textColor=HexColor('#3F51B5'))) # Azul médio
    styles.add(ParagraphStyle(name='SummaryTitle', 
                           fontSize=16, 
                           leading=20, 
                           fontName='DejaVuSans-Bold', 
                           alignment=TA_LEFT, 
                           spaceAfter=4,
                           textColor=HexColor('#212121'))) # Título do Sumário
    styles.add(ParagraphStyle(name='SummaryText', 
                           fontSize=10, 
                           leading=14, 
                           fontName='DejaVuSans', 
                           spaceAfter=4,
                           textColor=HexColor('#424242'))) # Texto do Sumário
    styles.add(ParagraphStyle(name='PostTitle', fontSize=14, bold=True, backColor=colors.lightgrey, borderWidth=0.5, borderColor=colors.grey, borderPadding=6))
    # Novo estilo para o bloco de post (para ser usado com Table)
    styles.add(ParagraphStyle(name='PostSection',
                            fontSize=11,
                            leading=14,
                            spaceAfter=0,
                            fontName='DejaVuSans',
                            backColor=HexColor('#F5F5F5'), # Cinza muito claro
                            borderPadding=10,
                            borderRadius=6,
                            borderColor=HexColor('#E0E0E0'),
                            borderWidth=1))

    # Ajuste no PostSubtitle para usar a cor primária
    styles.add(ParagraphStyle(name='PostSubtitle',
                            fontSize=12,
                            leading=16,
                            fontName='DejaVuSans-Bold',
                            spaceBefore=0,
                            spaceAfter=0,
                            textColor=HexColor('#1A237E'))) # Azul escuro primário
    styles.add(ParagraphStyle(name='ColoredPostSubtitle', # Novo estilo para subtítulos coloridos (azul)
                           fontSize=12, 
                           leading=16, 
                           fontName='DejaVuSans-Bold', 
                           spaceBefore=0, 
                           spaceAfter=0,
                           textColor=HexColor('#3F51B5'))) # Azul médio para subtítulos
    styles.add(ParagraphStyle(name='NeutralPostSubtitle', fontName='DejaVuSans-Bold', fontSize=11, leading=12, textColor=colors.HexColor('#616161')))
    styles.add(ParagraphStyle(name='BlackSubtitle', fontName='DejaVuSans-Bold', fontSize=11, leading=12, textColor=colors.black))
    styles.add(ParagraphStyle(name='PurpleSubtitle', fontName='DejaVuSans-Bold', fontSize=11, leading=12, textColor=colors.HexColor('#800080')))
    styles.add(ParagraphStyle(name='StrongPurpleSubtitle', fontName='DejaVuSans-Bold', fontSize=11, leading=12, textColor=colors.HexColor('#6A0DAD')))
    styles.add(ParagraphStyle(name='DarkGreenSubtitle', fontName='DejaVuSans-Bold', fontSize=11, leading=12, textColor=colors.HexColor('#006400')))
    styles.add(ParagraphStyle(name='BrownSubtitle', fontName='DejaVuSans-Bold', fontSize=11, leading=12, textColor=colors.HexColor('#A52A2A')))
    styles.add(ParagraphStyle(name='PostText', 
                           fontSize=10, 
                           leading=14, 
                           fontName='DejaVuSans', 
                           spaceAfter=0,
                           textColor=HexColor('#424242'))) # Texto do Post
    styles.add(ParagraphStyle(name='PostContent', # Novo estilo para o conteúdo das subsessões
                           fontSize=10, 
                           leading=14, 
                           fontName='DejaVuSans', 
                           spaceAfter=0,
                           leftIndent=12, # Recuo para o conteúdo
                           textColor=HexColor('#424242'))) 
    styles.add(ParagraphStyle(name='PostHashtag', 
                           fontSize=10, 
                           leading=14, 
                           fontName='DejaVuSans-Bold',
                           textColor=HexColor('#3F51B5'))) # Hashtag do Post
    styles.add(ParagraphStyle(name='PostFormat', 
                           fontSize=10, 
                           leading=14, 
                           fontName='DejaVuSans-Oblique', 
                           spaceAfter=0,
                           textColor=HexColor('#616161'))) # Formato do Post
    styles.add(ParagraphStyle(name='PostVisuals', 
                           fontSize=10, 
                           leading=14, 
                           fontName='DejaVuSans', 
                           spaceAfter=0,
                           textColor=HexColor('#424242'))) # Sugestões Visuais do Post
    styles.add(ParagraphStyle(name='ChecklistTitle', 
                               fontSize=16, 
                               leading=20, 
                               fontName='DejaVuSans-Bold', 
                               spaceAfter=10,
                               textColor=HexColor('#212121'))) # Título do Checklist
    styles.add(ParagraphStyle(name='ChecklistItem', 
                               fontSize=11, 
                               leading=16, 
                               spaceBefore=4,
                               fontName='DejaVuSans',
                               textColor=HexColor('#212121'))) # Item do Checklist
    # Estilo para datas no checklist
    styles.add(ParagraphStyle(name='ChecklistDate', 
                               fontSize=12, 
                               leading=16, 
                               spaceBefore=10, 
                               fontName='DejaVuSans-Bold',
                               textColor=HexColor('#000000'))) # Preto
    styles.add(ParagraphStyle(name='CalendarTitle', 
                               fontSize=16, 
                               leading=20, 
                               fontName='DejaVuSans-Bold', 
                               spaceAfter=10,
                               textColor=HexColor('#212121'))) # Título do Calendário
    styles.add(ParagraphStyle(name='CalendarHeader', 
                               fontSize=12, 
                               leading=16, 
                               fontName='DejaVuSans-Bold', 
                               spaceAfter=6,
                               textColor=HexColor('#424242'))) # Cabeçalho do Calendário
    styles.add(ParagraphStyle(name='CalendarEntry', 
                               fontSize=10, 
                               leading=14, 
                               fontName='DejaVuSans', 
                               spaceAfter=4,
                               textColor=HexColor('#424242'))) # Entrada do Calendário
    
    # Para tables
    styles.add(ParagraphStyle(name='TableHeader', fontSize=12, bold=True, alignment=TA_CENTER, textColor=HexColor('#FFFFFF'), backColor=HexColor('#1A237E')))
    styles.add(ParagraphStyle(name='TableCell', fontSize=10, alignment=TA_LEFT, textColor=HexColor('#000000')))
    
    # Para charts (titles)
    styles.add(ParagraphStyle(name='ChartTitle', fontSize=14, bold=True, alignment=TA_CENTER, spaceAfter=10, textColor=HexColor('#3F51B5')))

    styles.add(ParagraphStyle(name='TableGradientStyle', parent=styles['Normal']))
    styles['TableGradientStyle']._table_style = get_table_style_for_gradient_row()
    
    return styles

def get_table_style_for_gradient_row():
    from reportlab.platypus import TableStyle
    from reportlab.lib.colors import HexColor
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E8EAF6')),  # Single color for entire table
    ])

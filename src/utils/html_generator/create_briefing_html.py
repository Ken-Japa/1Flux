import json
from datetime import datetime
from src.utils.pdf_generator.calendar_logic import generate_publication_calendar
from src.utils.pdf_generator.checklist_logic import generate_publication_checklist
from markdown import markdown
import textwrap
from bs4 import BeautifulSoup

def create_briefing_html(content_json: dict, client_name: str, output_filename: str = "briefing.html", target_audience: str = "", tone_of_voice: str = "", marketing_objectives: str = "", future_strategy: str = "", market_references: list = None, suggested_metrics: dict = None):
    """
    Gera um arquivo HTML de briefing profissional a partir de um JSON de conteúdo.
    O `content_json` deve conter uma lista de posts dentro da chave 'generated_content' -> 'posts'.
    Recomenda-se que o JSON contenha 5 posts para um briefing semanal.

    Args:
        content_json (dict): O JSON contendo os dados do conteúdo gerado.
        client_name (str): O nome do cliente para o qual o briefing está sendo gerado.
        output_filename (str): O nome do arquivo HTML de saída. Padrão é "briefing.html".
        target_audience (str): O público-alvo do briefing.
        tone_of_voice (str): O tom de voz a ser utilizado no briefing.
        marketing_objectives (str): Os objetivos de marketing do briefing.
    """
    # Formatar todo o JSON para suportar Markdown
    content_json = formatar_json_markdown(content_json)

    # Determine the generation date
    generation_date_str = content_json.get("generation_date")
    if not generation_date_str:
        generation_date_str = content_json.get("generated_content", {}).get("generation_date")
    if not generation_date_str:
        generation_date_str = datetime.now().strftime("%d/%m/%Y")

    # --- Sumário Executivo ---
    weekly_strategy_summary_content = content_json.get('weekly_strategy_summary', '')
    if isinstance(weekly_strategy_summary_content, str):
        try:
            weekly_strategy_summary_dict = json.loads(weekly_strategy_summary_content)
        except json.JSONDecodeError:
            weekly_strategy_summary_dict = {'summary': weekly_strategy_summary_content}
    elif isinstance(weekly_strategy_summary_content, dict):
        weekly_strategy_summary_dict = weekly_strategy_summary_content
    else:
        weekly_strategy_summary_dict = {}

    summary_html = ""
    if weekly_strategy_summary_dict:
        summary_html += "        <h2>Sumário Executivo</h2>\n"
        summary_html += f"        <p>{weekly_strategy_summary_dict.get('summary', 'N/A')}</p>\n"
        
        future_strategy = content_json.get('future_strategy', '')
        if future_strategy and isinstance(future_strategy, dict):
            summary_html += "        <h3>Sugestões para Depois da Campanha:</h3>\n"
            if 'proximos_passos' in future_strategy:
                summary_html += f"        <p>{future_strategy['proximos_passos']}</p>\n"
            if 'posts_nutricao' in future_strategy:
                summary_html += "        <h4>Posts de Nutrição:</h4>\n        <ul>\n"
                for p in future_strategy['posts_nutricao']:
                    summary_html += f"            <li><strong>{p.get('tema', 'N/A')}</strong> - {p.get('formato', 'N/A')} - {p.get('objetivo', 'N/A')}</li>\n"
                summary_html += "        </ul>\n"
            if 'remarketing' in future_strategy:
                summary_html += "        <h4>Estratégias de Remarketing:</h4>\n        <ul>\n"
                for r in future_strategy['remarketing']:
                    summary_html += f"            <li><strong>{r.get('estrategia', 'N/A')}</strong> - Canal: {r.get('canal', 'N/A')}</li>\n"
                summary_html += "        </ul>\n"
        elif future_strategy:
            summary_html += f"        <h3>Sugestões para Depois da Campanha:</h3><p>{future_strategy}</p>\n"

        market_references = content_json.get('market_references', []) 
        if market_references:
            summary_html += f"        <h3>Análise de Concorrentes e Referências de Sucesso:</h3>\n"
            summary_html += "        <ul class=\"competitor-list\">\n"
            for ref in market_references:
                summary_html += f"            <li><strong>Nome/Handle:</strong> {ref.get('Nome/Handle', 'N/A')}<br>\n\n"
                summary_html += f"                <strong>Diferenciais:</strong> {ref.get('Diferenciais', 'N/A')}<br>\n\n"
                summary_html += f"                <strong>Oportunidades:</strong> {ref.get('Oportunidades', 'N/A')}<br>\n\n"
                summary_html += f"                <strong>Posicionamento do Cliente:</strong> {ref.get('Posicionamento do Cliente', 'N/A')}</li>\n\n"
            summary_html += "        </ul>\n"

        if target_audience:
            summary_html += f"        <h3>Público-Alvo:</h3><p>{target_audience}</p>\n"
        if tone_of_voice:
            summary_html += f"        <h3>Tom de Voz:</h3><p>{tone_of_voice}</p>\n"
        if marketing_objectives:
            summary_html += f"        <h3>Objetivos de Marketing:</h3><p>{marketing_objectives}</p>\n"

    # --- Métricas Sugeridas ---
    metrics_html = ""

    if suggested_metrics:
        metrics_html += "        <h2>Métricas Sugeridas</h2>\n"
        metrics_html += f"        <h3>Objetivo Principal:</h3><p>{suggested_metrics.get("objetivo_principal", "N/A")}</p>\n"
        if suggested_metrics.get("indicadores_chave"):
            metrics_html += "        <h3>Indicadores Chave:</h3>\n"
            metrics_html += "        <ul>\n"
            for indicador in suggested_metrics["indicadores_chave"]:
                metrics_html += f"            <li>{indicador}</li>\n"
            metrics_html += "        </ul>\n"
        if suggested_metrics.get("metricas_secundarias"):
            metrics_html += "        <h3>Métricas Secundárias:</h3>\n"
            metrics_html += "        <ul>\n"
            for metrica in suggested_metrics["metricas_secundarias"]:
                metrics_html += f"            <li>{metrica}</li>\n"
            metrics_html += "        </ul>\n"

    # --- Calendário de Publicação ---
    today = datetime.now()
    posts = content_json.get('posts', [])
    publication_calendar = generate_publication_calendar(today, posts)

    calendar_html = ""
    if publication_calendar:
        calendar_html += "        <h2>Calendário de Publicação</h2>\n"
        calendar_html += "        <table class=\"calendar-table\">\n"
        calendar_html += "            <thead>\n"
        calendar_html += "                <tr><th>Dia</th><th>Data</th><th>Horário</th><th>Post</th></tr>\n"
        calendar_html += "            </thead>\n"
        calendar_html += "            <tbody>\n"
        for entry in publication_calendar:
            for sub_entry in entry['entries']:
                calendar_html += f"                <tr><td>{entry['day'].split(', ')[0]}</td><td>{entry['day'].split(', ')[1]}</td><td>{sub_entry['time']}</td><td>{sub_entry['content']}</td></tr>\n"
        calendar_html += "            </tbody>\n"
        calendar_html += "        </table>\n"

    # --- Checklist de Publicação ---
    publication_checklist = generate_publication_checklist(publication_calendar)
    checklist_html = ""
    if publication_checklist:
        checklist_html += "        <h2>Checklist de Publicação</h2>\n"
        checklist_html += "        <ul class=\"checklist\">\n"
        for day_entry in publication_checklist:
            checklist_html += f"            <li><strong>{day_entry['date']}</strong></li>\n"
            checklist_html += "            <ul>\n"
            for task in day_entry['tasks']:
                # Prioridade: Postar (negrito), Preparar, Responder comentários
                task_type = task['type']
                task_title = formatar_texto_markdown(task['title'])
                if "Postar" in task_type:
                    checklist_html += f"                <li><strong>{task_type} Post #{task['post_number']}: {task_title}</strong></li>\n"
                else:
                    checklist_html += f"                <li>{task_type} Post #{task['post_number']}: {task_title}</li>\n"
            checklist_html += "            </ul>\n"
        checklist_html += "        </ul>\n"


    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roteiro de Publicações para {client_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {{ font-family: 'Roboto', sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4; }}
        .container {{ width: 80%; margin: 20px auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        /* Capa - Mudar para a cor primária do PDF */
        .cover {{
            text-align: center;
            padding: 50px 0;
            background: linear-gradient(to bottom, #1A237E, #3949AB);
            color: #fff;
            border-radius: 8px 8px 0 0;
            margin-bottom: 30px;
        }}
        .cover h1 {{ margin: 0; font-size: 2.5em; }}
        .cover p {{ margin: 0; font-size: 1.2em; margin-top: 10px; }}
        /* Títulos de Seção */
        h1, h2, h3 {{
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        h2 {{
            color: #1A237E; /* Azul Escuro */
            border-bottom: 3px solid #5C6BC0; /* Azul Médio */
            padding-bottom: 10px;
            margin-top: 40px;
            font-size: 1.8em;
        }}
        /* Bloco de Post */
        .post-section {{
            background-color: #F5F5F5; /* Cinza muito claro */
            border-left: 6px solid #1A237E; /* Linha de destaque */
            padding: 25px;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05); /* Sombra sutil */
        }}
        /* Subtítulos dentro do Post */
        .post-section h3 {{
            color: #1A237E; /* Azul Escuro */
            border-bottom: 1px solid #E0E0E0;
            padding-bottom: 5px;
            margin-top: 0;
            margin-bottom: 15px;
        }}
        .post-section .subtitulo-grupo1 strong:first-child {{ color: #1A237E !important; }} /* Azul Escuro */
        .post-section .subtitulo-grupo2 strong:first-child {{ color: #5C6BC0 !important; }} /* Azul Médio */
        .post-section .subtitulo-grupo3 strong:first-child {{ color: #2E7D32 !important; }} /* Verde */
        .post-section .subtitulo-grupo4 strong:first-child {{ color: #555555 !important; }} /* Cinza Escuro */
        /* Destaque para os rótulos (Tema, Legenda, etc.) – agora específico para labels */
        .post-section p > strong:first-child {{
            
            font-weight: 700;
            text-transform: uppercase;
            font-size: 1.1em;
        }}
        /* Reset para strong internos (no texto Markdown) */
        .post-section p strong:not(:first-child) {{
            color: inherit; /* Sem cor extra */
            text-transform: none; /* Sem uppercase */
            font-size: inherit; /* Tamanho normal */
        }}
        .checklist {{ list-style-type: none; padding: 0; }}
        .checklist li {{ background: #f0f0f0; margin-bottom: 5px; padding: 10px; border-radius: 3px; }}
        .checklist li:before {{ content: "\\f058"; font-family: "Font Awesome 6 Free"; color: #2E7D32; font-weight: bold; margin-right: 8px; }}
        em {{
            font-style: italic;
            color: #5C6BC0;
        }}
        .calendar-table {{ width: 100%; border-collapse: separate; border-spacing: 2px; margin-top: 20px; }}
        .calendar-table th, .calendar-table td {{ border: 2px solid #333; padding: 12px; text-align: left; }}
        .calendar-table th {{ background-color: #3F51B5; color: #fff; position: relative; }} /* Cabeçalho mais vibrante */
        .calendar-table th:before {{ font-family: "Font Awesome 6 Free"; margin-right: 8px; }} /* Ícone de calendário em th */
        .calendar-table td:first-child {{ font-weight: bold; color: #1A237E; }} /* Bold em dias */
        .calendar-table tr:nth-child(even) {{ background-color: #E8EAF6; }} /* Azul claro alternado */
        .calendar-table tr:hover {{ background-color: #C5CAE9; transition: background 0.3s; }} /* Hover para destaque */
        .footer {{
            width: 100%;
            margin-top: 50px;
            font-size: 0.9em;
            color: #777;
            border-top: 1px solid #ddd;
            padding-top: 20px;
        }}
        .footer p {{
            display: block;
            text-align: right;
        }}
        .checklist li {{ padding: 12px; margin-bottom: 8px; display: flex; align-items: center; }}
        .checklist ul {{ margin-left: 20px; list-style-type: disc; }} /* Sub-listas com bullets */
        ul.competitor-list li {{ border-bottom: 1px solid #E0E0E0; padding-bottom: 10px; margin-bottom: 10px; }}
        ul.competitor-list li:before {{ content: "\\f091"; font-family: "Font Awesome 6 Free"; color: #FF5722; margin-right: 8px; }} /* Ícone de trophy para refs */
        details {{ margin-bottom: 15px; }}
        summary {{ cursor: pointer; font-weight: bold; color: #5C6BC0; }}
        .post-section p strong:before {{ font-family: "Font Awesome 6 Free"; margin-right: 6px; }}
        .post-section p strong[data-icon="theme"]:before {{ content: "\\f249"; }}
        .post-section p strong[data-icon="cta"]:before {{ content: "\\f0a1"; }}
        .post-section p {{ word-break: break-word; max-width: 100%; }}
        @media print {{
            .container {{ width: 100%; box-shadow: none; }}
            .cover {{ page-break-after: always; }}
            .post-section {{ page-break-inside: avoid; }}
        }}
        @media (max-width: 768px) {{
            .container {{ width: 95%; padding: 15px; }}
            .post-section {{ padding: 15px; }}
            .calendar-table {{ font-size: 0.9em; }}
            .calendar-table th, .calendar-table td {{ padding: 8px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="cover">
            <h1>Briefing de Conteúdo Profissional</h1>
            <p>Para: {client_name}</p>
            <p>Data: {generation_date_str}</p>
        </div>

        <h2>Visão Geral do Conteúdo</h2>
        <p>Este documento apresenta o conteúdo sugerido para as redes sociais do cliente, com base nas diretrizes fornecidas e no perfil do público-alvo.</p>

        {summary_html}
        {calendar_html}

        <h2>Posts Sugeridos</h2>
        """
        
    subtitulo_grupos = {
    'Tema:': 'subtitulo-grupo1',
    'Justificativa Estratégica:': 'subtitulo-grupo1',
    'Micro Briefing:': 'subtitulo-grupo1',
    'Legenda Principal:': 'subtitulo-grupo2',
    'Variações de Legenda:': 'subtitulo-grupo2',
    'Hashtags:': 'subtitulo-grupo2',
    'Indicador Principal:': 'subtitulo-grupo2',
    'CTA Individual:': 'subtitulo-grupo3',
    'Sugestões de Interação/Engajamento:': 'subtitulo-grupo3',
    'Roteiro de Respostas a Comentários:': 'subtitulo-grupo3',
    'Sugestões Visuais:': 'subtitulo-grupo4',
    'Texto na Imagem/Vídeo:': 'subtitulo-grupo4',
    'Formato Sugerido:': 'subtitulo-grupo4',
    'Prompt para IA Geradora de Imagens:': 'subtitulo-grupo4',
    'Testes A/B:': 'subtitulo-grupo4',
    'Como Corrigir a Rota (Gatilhos de Otimização):': 'subtitulo-grupo4',
    'Checklist de Publicação:': 'subtitulo-grupo4'
}

    # Adiciona os posts dinamicamente
    for i, post in enumerate(content_json.get("posts", [])):
        html_content += f"""
            <div class="post-section">
                <h3>Post #{i + 1}: {post.get("titulo", "Sem Título")}</h3>
               <p class="{subtitulo_grupos.get('Tema:', '')}"><strong>Tema:</strong> {post.get("tema", "N/A")}</p>
                <p class="{subtitulo_grupos.get('Justificativa Estratégica:', '')}"><strong>Justificativa Estratégica:</strong> {post.get("post_strategy_rationale", "N/A")}</p>
                <p class="{subtitulo_grupos.get('Micro Briefing:', '')}"><strong>Micro Briefing:</strong> {post.get("micro_briefing", "N/A")}</p>
                <p class="{subtitulo_grupos.get('Legenda Principal:', '')}"><strong>Legenda Principal:</strong> {post.get("legenda_principal", "N/A")}</p>
                <details>
                    <summary style="text-decoration: underline; font-style: italic; color: #FFA500;">Clique para expandir variações</summary>
                    <p><strong>Variações:</strong></p>
                    <ul>
        """
        for variation in post.get("variacoes_legenda", []):
            html_content += f"                    <li>{variation}</li>\n"
        html_content += f"""
                    </ul>
                </details>
                <p class="{subtitulo_grupos.get('Hashtags:', '')}"><strong>Hashtags:</strong> {" ".join(post.get("hashtags", []))}</p>
                <p class="{subtitulo_grupos.get('Indicador Principal:', '')}"><strong>Indicador Principal:</strong> {post.get("indicador_principal", "N/A")}</p>
                <p class="{subtitulo_grupos.get('CTA Individual:', '')}"><strong>CTA Individual:</strong> {post.get("cta_individual", "N/A")}</p>
                <p class="{subtitulo_grupos.get('Sugestões de Interação/Engajamento:', '')}"><strong>Sugestões de Interação/Engajamento:</strong> {post.get("interacao", "N/A")}</p>
        """
        response_script = post.get("response_script", [])
        if response_script:
            html_content += f"""
                <details>
                    <summary style="text-decoration: underline; font-style: italic; color: #FFA500;">Clique para expandir roteiro de respostas</summary>
                    <p><strong>Roteiro de Respostas:</strong></p>
                    <ul>
            """
            for script_item in response_script:
                html_content += f"                    <li><strong>Comentário Genérico:</strong> {script_item.get('comentario_generico', 'N/A')}<br>\n"
                html_content += f"                        <strong>Resposta Sugerida:</strong> {script_item.get('resposta_sugerida', 'N/A')}</li>\n"
                html_content += f"                    <li><strong>Comentário Negativo:</strong> {script_item.get('comentario_negativo', 'N/A')}<br>\n"
                html_content += f"                        <strong>Resposta para Negativo:</strong> {script_item.get('resposta_negativo', 'N/A')}</li>\n"
            html_content += f"""
                    </ul>
                </details>
            """
        html_content += f"""
                {f'<p class="{subtitulo_grupos.get("Sugestões Visuais:", "")}"><strong>Sugestões Visuais:</strong> {post.get("visual_description_portuguese", "N/A")}</p>' if post.get("visual_description_portuguese") else ""}
                {f'<p class="{subtitulo_grupos.get("Texto na Imagem/Vídeo:", "")}"><strong>Texto na Imagem/Vídeo:</strong> {post.get("text_in_image", "N/A")}</p>' if post.get("text_in_image") else ""}
                <p class="{subtitulo_grupos.get('Formato Sugerido:', '')}"><strong>Formato Sugerido:</strong> {post.get("sugestao_formato", "N/A")}</p>
        
        """
        if post.get("carrossel_slides") and len(post["carrossel_slides"]) > 0:
            html_content += f"""
                <h4>Slides do Carrossel:</h4>
                <ol>
            """
            for slide in post.get("carrossel_slides", []):
                html_content += f"                    <li><strong>{slide.get("titulo_slide", "")}</strong>: {slide.get("texto_slide", "")} (Visual: {slide.get("sugestao_visual_slide", "")})</li>\n"
            html_content += f"""
                </ol>
            """
        elif post.get("micro_roteiro") and len(post["micro_roteiro"]) > 0:
            html_content += f"""
                <h4>Micro Roteiro (Vídeo):</h4>
                <ol>
            """
            for cena in post.get("micro_roteiro", []):
                html_content += f"                    <li><strong>Cena:</strong> {cena.get("cena", "")} - <strong>Descrição Visual:</strong> {cena.get("descricao", "")} - <strong>Fala:</strong> {cena.get("fala", "")}</li>\n"
            html_content += f"""
                </ol>
            """
        html_content += f"""
                {f'<p class="{subtitulo_grupos.get("Prompt para IA Geradora de Imagens:", "")}"><strong>Prompt para IA Geradora de Imagens:</strong> {post.get("visual_prompt_suggestion", "N/A")}</p>' if post.get("visual_prompt_suggestion") else ""}
                {f'<p class="{subtitulo_grupos.get("Testes A/B:", "")}"><strong>Testes A/B:</strong> {post.get("ab_test_suggestions", "N/A")}</p>' if post.get("ab_test_suggestions") else ""}
                {f'<p class="{subtitulo_grupos.get("Como Corrigir a Rota (Gatilhos de Otimização):", "")}"><strong>Como Corrigir a Rota (Gatilhos de Otimização):</strong> {post.get("optimization_triggers", "N/A")}</p>' if post.get("optimization_triggers") else ""}
                <p class="{subtitulo_grupos.get('Checklist de Publicação:', '')}"><strong>Checklist de Publicação:</strong></p>
                <ul class="checklist">
                    <li>Revisar texto e gramática.</li>
                    <li>Verificar a qualidade da imagem/vídeo.</li>
                    <li>Confirmar o agendamento.</li>
                    <li>Responder a comentários e mensagens.</li>
                </ul>
            </div>
        """
    html_content += f"""
        {metrics_html}
        {checklist_html}
"""

    # Adiciona o rodapé e fechamento do HTML
    html_content += """
            <div class="footer">
                <p>&copy; 2025 Conteúdo gerado por Fluxo Criativo. Todos os direitos reservados.</p>
            </div>
        </div>
    </body>
</html>
    """

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)



def formatar_texto_markdown(texto):
    """Converte Markdown para HTML inline, removendo wrappers externos e indentação."""
    if not texto or not isinstance(texto, str):
        return texto
    
    # Remove indentação e strip
    texto = textwrap.dedent(texto).strip()
    
    # Converte para HTML
    html = markdown(texto, extensions=['extra', 'nl2br'])
    
    # Parse com BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove wrapper externo
    block = soup.find(['p', 'ul', 'ol', 'pre', 'code', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    if block:
        inner_html = ''.join(str(child) for child in block.children if child).strip()
    else:
        inner_html = str(soup).strip()
    
    # Para hashtags: Se começar com #, escapa para não virar <h1>
    if inner_html.startswith('<h1>'):
        inner_html = inner_html.replace('<h1>', '', 1).replace('</h1>', '', 1)
    
    return inner_html
    
    return inner_html

def formatar_json_markdown(content_json):
    content_json = content_json.copy()
    # Campos de nível superior
    if 'weekly_strategy_summary' in content_json and isinstance(content_json['weekly_strategy_summary'], str):
        content_json['weekly_strategy_summary'] = formatar_texto_markdown(content_json['weekly_strategy_summary'])
    
    # Future strategy: Se dict, formatar cada valor
    if 'future_strategy' in content_json and isinstance(content_json['future_strategy'], dict):
        fs = content_json['future_strategy']
        if 'proximos_passos' in fs:
            fs['proximos_passos'] = formatar_texto_markdown(fs['proximos_passos'])
        if 'posts_nutricao' in fs:
            for p in fs['posts_nutricao']:
                for k in ['tema', 'formato', 'objetivo']:
                    if k in p:
                        p[k] = formatar_texto_markdown(p[k])
        if 'remarketing' in fs:
            for r in fs['remarketing']:
                for k in ['estrategia', 'canal']:
                    if k in r:
                        r[k] = formatar_texto_markdown(r[k])
    
    # Posts
    for post in content_json.get('posts', []):
        campos_texto = [
            'titulo', 'tema', 'post_strategy_rationale', 'micro_briefing',
            'legenda_principal', 'cta_individual', 'interacao',
            'visual_description_portuguese', 'text_in_image',
            'visual_prompt_suggestion', 'ab_test_suggestions', 'optimization_triggers'
        ]
        for campo in campos_texto:
            if campo in post and isinstance(post[campo], str):
                post[campo] = formatar_texto_markdown(post[campo])
        
        # Variações
        if 'variacoes_legenda' in post:
            post['variacoes_legenda'] = [formatar_texto_markdown(var) for var in post['variacoes_legenda']]
        
        # Hashtags: Não formatar (evita # virar <h1>)
        pass
        
        # Response script
        if 'response_script' in post:
            for script_item in post['response_script']:
                for key in ['comentario_generico', 'resposta_sugerida', 'comentario_negativo', 'resposta_negativo']:
                    if key in script_item:
                        script_item[key] = formatar_texto_markdown(script_item[key])
        
        # Carrossel slides
        if 'carrossel_slides' in post:
            for slide in post['carrossel_slides']:
                for key in ['titulo_slide', 'texto_slide', 'sugestao_visual_slide']:
                    if key in slide:
                        slide[key] = formatar_texto_markdown(slide[key])
        
        # Micro roteiro
        if 'micro_roteiro' in post:
            for cena in post['micro_roteiro']:
                for key in ['cena', 'descricao', 'fala']:
                    if key in cena:
                        cena[key] = formatar_texto_markdown(cena[key])
    
    # Métricas
    if 'suggested_metrics' in content_json:
        if 'objetivo_principal' in content_json['suggested_metrics']:
            content_json['suggested_metrics']['objetivo_principal'] = formatar_texto_markdown(content_json['suggested_metrics']['objetivo_principal'])
        for key in ['indicadores_chave', 'metricas_secundarias']:
            if key in content_json['suggested_metrics']:
                content_json['suggested_metrics'][key] = [formatar_texto_markdown(item) for item in content_json['suggested_metrics'][key]]
    
    return content_json
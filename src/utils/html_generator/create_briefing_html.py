import json
from datetime import datetime
from src.utils.pdf_generator.calendar_logic import generate_publication_calendar
from src.utils.pdf_generator.checklist_logic import generate_publication_checklist

def create_briefing_html(content_json: dict, client_name: str, output_filename: str = "briefing.html", target_audience: str = "", tone_of_voice: str = "", marketing_objectives: str = "", future_strategy: str = "", market_references: list = None):
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
        if future_strategy:
            summary_html += f"        <h3>Sugestões para Depois da Campanha:</h3><p>{future_strategy}</p>\n"

        market_references = content_json.get('market_references', []) 
        if market_references:
            summary_html += f"        <h3>Análise de Concorrentes e Referências de Sucesso:</h3>\n"
            summary_html += "        <ul>\n"
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
    suggested_metrics = content_json.get("metricas_de_sucesso_sugeridas", {})

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
        calendar_html += "            <tbody>\n        """
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
                task_title = task['title']
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
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f4; }}
        .container {{ width: 80%; margin: 20px auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        /* Capa - Mudar para a cor primária do PDF */
        .cover {{
            text-align: center;
            padding: 50px 0;
            background-color: #1A237E; /* Azul Escuro */
            color: #fff;
            border-radius: 8px 8px 0 0;
            margin-bottom: 30px;
        }}
        .cover h1 {{ margin: 0; font-size: 2.5em; }}
        .cover p {{ font-size: 1.2em; margin-top: 10px; }}
        /* Títulos de Seção */
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
            padding: 20px;
            margin-bottom: 25px;
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
        /* Destaque para os rótulos (Tema, Legenda, etc.) */
        .post-section p strong {{
            color: #5C6BC0; /* Azul Médio */
        }}
        .checklist {{ list-style-type: none; padding: 0; }}
        .checklist li {{ background: #f0f0f0; margin-bottom: 5px; padding: 10px; border-radius: 3px; }}
        .checklist li:before {{ content: "✅ "; color: #2E7D32; font-weight: bold; }} /* Ou "☐ " se for para ser preenchido */
        .calendar-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .calendar-table th, .calendar-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .calendar-table th {{ background-color: #F5F5F5; }} /* Fundo claro para o cabeçalho da tabela */
        .footer {{ text-align: center; margin-top: 50px; font-size: 0.9em; color: #777; }}
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

    # Adiciona os posts dinamicamente
    for i, post in enumerate(content_json.get("posts", [])):
        html_content += f"""
            <div class="post-section">
                <h3>Post #{i + 1}: {post.get("titulo", "Sem Título")}</h3>
                {f"<p><strong>Tema:</strong> {post.get("tema", "N/A")}</p>" if post.get("tema") else ""}
                <p><strong>Justificativa Estratégica:</strong> {post.get("post_strategy_rationale", "N/A")}</p>
                <p><strong>Briefing:</strong> {post.get("micro_briefing", "N/A")}</p>
                <p><strong>Legenda:</strong> {post.get("legenda_principal", "N/A")}</p>
                <p><strong>Variações:</strong></p>
                <ul>
        """
        for variation in post.get("variacoes_legenda", []):
            html_content += f"                    <li>{variation}</li>\n"
        html_content += f"""
                </ul>
                {f"<p><strong>Hashtags:</strong> {" ".join(post.get("hashtags", []))}</p>" if post.get("hashtags") else ""}
                {f"<p><strong>Indicador Principal:</strong> {post.get("indicador_principal", "N/A")}</p>" if post.get("indicador_principal") else ""}
                {f"<p><strong>Chamada para Ação (CTA):</strong> {post.get("cta_individual", "N/A")}</p>" if post.get("cta_individual") else ""}
                {f"<p><strong>Sugestões de Interação/Engajamento:</strong> {post.get("interacao", "N/A")}</p>" if post.get("interacao") else ""}
        """
        response_script = post.get("response_script", [])
        if response_script:
            html_content += f"""
                <p><strong>Roteiro de Respostas:</strong></p>
                <ul>
            """
            for script_item in response_script:
                html_content += f"                    <li><strong>Comentário Genérico:</strong> {script_item.get('comentario_generico', 'N/A')}<br>"
                html_content += f"                        <strong>Resposta Sugerida:</strong> {script_item.get('resposta_sugerida', 'N/A')}</li>\n"
                html_content += f"                    <li><strong>Comentário Negativo:</strong> {script_item.get('comentario_negativo', 'N/A')}<br>"
                html_content += f"                        <strong>Resposta para Negativo:</strong> {script_item.get('resposta_negativo', 'N/A')}</li>\n"
            html_content += f"""
                </ul>
            """
        html_content += f"""
                {f"<p><strong>Sugestões Visuais:</strong> {post.get("visual_description_portuguese", "N/A")}</p>" if post.get("visual_description_portuguese") else ""}
                {f"<p><strong>Texto na Imagem/Vídeo:</strong> {post.get("text_in_image", "N/A")}</p>" if post.get("text_in_image") else ""}
                <p><strong>Formato Sugerido:</strong> {post.get("sugestao_formato", "N/A")}</p>
        """
        if post.get("sugestao_formato") == "Carrossel de imagens":
            html_content += f"""
                <h4>Slides do Carrossel:</h4>
                <ol>
            """
            for slide in post.get("carrossel_slides", []):
                html_content += f"                    <li><strong>{slide.get("titulo_slide", "")}</strong>: {slide.get("texto_slide", "")} (Visual: {slide.get("sugestao_visual_slide", "")})</li>\n"
            html_content += f"""
                </ol>
            """
        elif post.get("sugestao_formato") == "Vídeo":
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
                {f"<p><strong>Prompt para IA Geradora de Imagens:</strong> {post.get("visual_prompt_suggestion", "N/A")}</p>" if post.get("visual_prompt_suggestion") else ""}
                {f"<p><strong>Testes A/B:</strong> {post.get("ab_test_suggestions", "N/A")}</p>" if post.get("ab_test_suggestions") else ""}
                {f"<p><strong>Como Corrigir a Rota (Gatilhos de Otimização):</strong> {post.get("optimization_triggers", "N/A")}</p>" if post.get("optimization_triggers") else ""}
                <p><strong>Checklist de Publicação:</strong></p>
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
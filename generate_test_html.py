import json
from src.utils.html_generator.create_briefing_html import create_briefing_html

dummy_content_json = {
    "generation_date": "25/07/2024",
    "weekly_strategy_summary": {
        "summary": "Esta é uma estratégia semanal de exemplo para testar a geração de HTML."
    },
    "posts": [
        {
            "titulo": "Título do Post de Exemplo 1",
            "tema": "Marketing Digital",
            "post_strategy_rationale": "Aumentar o engajamento da audiência com conteúdo relevante.",
            "micro_briefing": "Criar um post sobre as últimas tendências em SEO.",
            "legenda_principal": "Descubra as novidades do SEO que vão impulsionar seu negócio! #SEO #MarketingDigital",
            "variacoes_legenda": [
                "Var. 1: Otimize seu site com as dicas de SEO mais recentes!",
                "Var. 2: Não fique para trás! As tendências de SEO que você precisa conhecer."
            ],
            "hashtags": ["#SEO", "#MarketingDigital", "#DicasDeSEO"],
            "indicador_principal": "Cliques no link",
            "cta_individual": "Saiba mais no nosso blog!",
            "interacao": "Pergunte aos seguidores qual a maior dificuldade em SEO.",
            "response_script": [
                {
                    "comentario_generico": "Ótimo conteúdo!",
                    "resposta_sugerida": "Obrigado! Fico feliz que tenha gostado."
                },
                {
                    "comentario_negativo": "Não concordo com essa estratégia.",
                    "resposta_negativo": "Agradecemos seu feedback. Qual sua perspectiva sobre o assunto?"
                }
            ],
            "visual_description_portuguese": "Infográfico com ícones modernos e cores vibrantes sobre SEO.",
            "text_in_image": "As 5 tendências de SEO para 2024",
            "sugestao_formato": "Imagem única",
            "visual_prompt_suggestion": "Infographic about SEO trends, modern design, vibrant colors, data visualization.",
            "ab_test_suggestions": "Testar diferentes CTAs no final da legenda.",
            "optimization_triggers": "Baixo engajamento: revisar horário de postagem e tipo de conteúdo."
        },
        {
            "titulo": "Título do Post de Exemplo 2",
            "tema": "Redes Sociais",
            "post_strategy_rationale": "Educar a audiência sobre o uso eficaz das redes sociais.",
            "micro_briefing": "Publicar dicas sobre como criar stories engajadores.",
            "legenda_principal": "Stories que prendem a atenção? Temos as dicas perfeitas para você! #Stories #RedesSociais",
            "variacoes_legenda": [
                "Var. 1: Transforme seus stories em um ímã de engajamento!",
                "Var. 2: Crie stories incríveis com estas dicas rápidas."
            ],
            "hashtags": ["#Stories", "#RedesSociais", "#DicasInstagram"],
            "indicador_principal": "Visualizações de Stories",
            "cta_individual": "Assista ao nosso tutorial completo!",
            "interacao": "Peça aos seguidores para compartilhar seus stories favoritos.",
            "response_script": [
                {
                    "comentario_generico": "Adorei as dicas!",
                    "resposta_sugerida": "Que bom que gostou! Qual sua dica favorita?"
                }
            ],
            "visual_description_portuguese": "Vídeo curto com transições rápidas mostrando exemplos de stories.",
            "text_in_image": "Stories que engajam: o segredo revelado",
            "sugestao_formato": "Vídeo",
            "micro_roteiro": [
                {"cena": "Abertura", "descricao": "Pessoa olhando o celular com expressão de tédio.", "fala": "Seus stories não engajam?"},
                {"cena": "Dica 1", "descricao": "Tela do celular mostrando um story com enquete.", "fala": "Use enquetes e perguntas!"}
            ],
            "visual_prompt_suggestion": "Short video, fast transitions, showing engaging Instagram stories examples, bright colors.",
            "ab_test_suggestions": "Testar diferentes músicas de fundo para o vídeo.",
            "optimization_triggers": "Baixas visualizações: experimentar diferentes ganchos nos primeiros segundos."
        }
    ]
}

output_file = "c:\\Users\\Ken\\Desktop\\Prog2\\Fluxo-Criativo\\briefing_test.html"

create_briefing_html(
    content_json=dummy_content_json,
    client_name="Cliente de Teste",
    output_filename=output_file,
    target_audience="Empreendedores digitais",
    tone_of_voice="Inspirador e informativo",
    marketing_objectives="Aumentar reconhecimento de marca e gerar leads"
)

print(f"HTML de teste gerado em {output_file}")
def generate_campaign_narrative(campaign_type: str) -> list[str]:
    """
    Gera a narrativa da campanha com base no tipo de campanha fornecido.

    Args:
        campaign_type (str): O tipo de campanha (e.g., "lancamento", "autoridade").

    Returns:
        list[str]: Uma lista de strings representando a narrativa da campanha.
    """
    narratives = {
        "lancamento": [
            "A campanha deve seguir uma narrativa progressiva ao longo dos 5 posts, abordando:",
            "- Post 1: Apresentação do Problema/Desafio do público-alvo.",
            "- Post 2: Introdução da Solução (produto/serviço do cliente).",
            "- Post 3: Detalhamento dos Benefícios e Vantagens da solução.",
            "- Post 4: Prova Social/Exemplos de Sucesso/Depoimentos.",
            "- Post 5: Chamada para Ação (CTA) clara e direta.",
        ],
        "autoridade": [
            "A campanha deve seguir uma narrativa progressiva ao longo dos 5 posts, abordando:",
            "- Post 1: Dica ou Insight da Semana: Conteúdo educativo com valor imediato.",
            "- Post 2: Bastidores: Mostrar como a solução é construída (processo, equipe, metodologia).",
            "- Post 3: Estudo de Caso: Provar resultados ou demonstrar expertise com um exemplo real.",
            "- Post 4: FAQ / Quebra de Objeções: Responder dúvidas comuns e reforçar autoridade.",
            "- Post 5: Evento ou CTA Premium: Convidar para um webinar, e-book, consultoria, etc.",
        ],
        "engajamento": [
            "A campanha deve seguir uma narrativa progressiva ao longo dos 5 posts, abordando:",
            "- Post 1: Enquete ou Pergunta: Criar uma conversa com o público.",
            "- Post 2: Peça de Opinião: Pedir que comentem ideias, dores ou experiências.",
            "- Post 3: Desafio ou Participação: Propor que executem algo (ex: “Desafio 7 dias”).",
            "- Post 4: Live ou Sessão de Q&A: Interação direta em tempo real.",
            "- Post 5: Resumo/Compilado: Mostrar as melhores respostas, resultados ou insights.",
        ],
        "conversao": [
            "A campanha deve seguir uma narrativa progressiva ao longo dos 5 posts, abordando:",
            "- Post 1: Atenção / Gancho Forte: Chamar atenção com um insight, dado ou pergunta direta.",
            "- Post 2: Problema: Reforçar a dor ou oportunidade perdida.",
            "- Post 3: Oferta: Apresentar a solução paga e seus diferenciais.",
            "- Post 4: Urgência / Escassez: Mostrar prazo, bônus ou vantagens limitadas.",
            "- Post 5: CTA Final: Levar diretamente ao cadastro, compra ou formulário.",
        ],
        "retencao": [
            "A campanha deve seguir uma narrativa progressiva ao longo dos 5 posts, abordando:",
            "- Post 1: Agradecimento: Mostrar reconhecimento ao usuário/cliente atual.",
            "- Post 2: Atualizações: Apresentar novidades e melhorias.",
            "- Post 3: Conteúdo Exclusivo: Dicas avançadas, tutoriais, bônus.",
            "- Post 4: Feedback: Pedir opiniões e sugestões.",
            "- Post 5: Comunidade: Convidar para grupo fechado, evento ou programa VIP.",
        ],
        "criativa": [
            "A lógica aqui não é seguir um arco narrativo de 5 posts conectados, mas sim gerar ideias independentes, originais e variadas, pensadas no estilo do criador.",
            "Lista de ideias → Formato → Objetivo → Estrutura resumida.",
        ],
    }
    return narratives.get(campaign_type.lower(), narratives["lancamento"])
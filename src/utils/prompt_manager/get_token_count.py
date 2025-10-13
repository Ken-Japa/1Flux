def get_token_count(prompt_text: str) -> int:
    """
    Estima o número de tokens de um prompt. Esta é uma estimativa simples
    baseada no número de palavras.

    Args:
        prompt_text (str): O texto do prompt.

    Returns:
        int: Número estimado de tokens.
    """
    # Uma estimativa simples: 1 token ~ 4 caracteres ou 0.75 palavras
    # Para maior precisão, seria necessário usar um tokenizador específico do modelo.
    return len(prompt_text.split()) # Contagem de palavras como estimativa
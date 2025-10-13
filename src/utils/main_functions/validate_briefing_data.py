def validate_briefing_data(brief_data: dict):
    """
    Valida os dados do briefing do cliente para garantir que todos os campos obrigatórios estejam presentes
    e com os tipos corretos.

    Args:
        brief_data (dict): Dicionário contendo os dados do briefing do cliente.

    Raises:
        ValueError: Se algum campo obrigatório estiver faltando ou for inválido.
    """
    required_fields = {
        "nome_do_cliente": str,
        "subnicho": str,
        "publico_alvo": str,
        "tom_de_voz": str,
        "objetivos_de_marketing": str,
        "chamada_para_acao": str,
        "tipo_de_conteudo": str,
        "conteudos_semanais": list
    }

    for field, expected_type in required_fields.items():
        if field not in brief_data:
            raise ValueError(f"Campo obrigatório '{field}' faltando no briefing do cliente.")
        if not isinstance(brief_data[field], expected_type):
            raise ValueError(f"Campo '{field}' deve ser do tipo {expected_type.__name__}, mas é {type(brief_data[field]).__name__}.")

    # Validação específica para conteudos_semanais
    if "conteudos_semanais" in brief_data:

        for i, item in enumerate(brief_data["conteudos_semanais"]):
            if not isinstance(item, dict):
                raise ValueError(f"Item {i} em 'conteudos_semanais' deve ser um dicionário.")
            if "objetivo_do_conteudo_individual" not in item:
                raise ValueError(f"Campo 'objetivo_do_conteudo_individual' faltando no item {i} de 'conteudos_semanais'.")
            if not isinstance(item["objetivo_do_conteudo_individual"], str):
                raise ValueError(f"Campo 'objetivo_do_conteudo_individual' no item {i} de 'conteudos_semanais' deve ser uma string.")
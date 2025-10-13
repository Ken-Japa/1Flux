import os
from src.data_storage import get_client_profile, insert_client_profile
from src.utils.data_storage.update_client_profile import update_client_profile

def get_or_create_client_profile(nome_do_cliente, informacoes_de_contato, publico_alvo, tom_de_voz, exemplos_de_nicho):
    """
    Verifica se um perfil de cliente existe no banco de dados. Se não existir, cria um novo perfil.
    Se existir, atualiza o perfil com os dados fornecidos.
    
    Args:
        nome_do_cliente (str): O nome do cliente.
        informacoes_de_contato (str): Informações de contato do cliente.
        publico_alvo (str): O público-alvo do cliente.
        tom_de_voz (str): O tom de voz preferido do cliente.
        exemplos_de_nicho (list): Exemplos de nicho do cliente.
        
    Returns:
        dict: O perfil do cliente (existente ou recém-criado/atualizado).
    """
    print(f"\nVerificando perfil para '{nome_do_cliente}'...")
    client_profile = get_client_profile(nome_do_cliente)

    if not client_profile:
        print(f"Perfil para '{nome_do_cliente}' não encontrado. Criando novo perfil...")
        insert_client_profile(
            client_name=nome_do_cliente,
            contact_info=informacoes_de_contato,
            public_target=publico_alvo,
            tone_of_voice=tom_de_voz,
            niche_examples=exemplos_de_nicho,
            status='active'
        )
        client_profile = get_client_profile(nome_do_cliente) # Recupera o perfil recém-criado
        print("Novo perfil de cliente criado.")
    else:
        print(f"Perfil para '{nome_do_cliente}' encontrado. Atualizando perfil existente com dados do briefing...")
        update_client_profile(
            client_name=nome_do_cliente,
            contact_info=informacoes_de_contato,
            public_target=publico_alvo,
            tone_of_voice=tom_de_voz,
            niche_examples=exemplos_de_nicho
        )
        client_profile = get_client_profile(nome_do_cliente) # Recupera o perfil atualizado
        print("Perfil de cliente existente atualizado.")
    
    return client_profile
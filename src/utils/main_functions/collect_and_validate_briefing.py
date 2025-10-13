import os
from src.utils.briefing_loader import load_briefing_from_json
from src.utils.main_functions.validate_briefing_data import validate_briefing_data

def collect_and_validate_briefing():
    """
    Coleta os dados do briefing do cliente a partir de um arquivo JSON e os valida.

    Returns:
        tuple: Uma tupla contendo (brief_data, nome_do_cliente, subnicho, informacoes_de_contato,
                     publico_alvo, tom_de_voz, exemplos_de_nicho, tipo_de_conteudo,
                     conteudos_semanais, objetivos_de_marketing) se o briefing for válido,
                     caso contrário, retorna None para todos os valores.
    """
    print("\n--- Coleta de Briefing do Cliente (via JSON) ---")
    briefing_filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'client_briefing.json')
    brief_data = load_briefing_from_json(briefing_filepath)

    if not brief_data:
        print("Não foi possível carregar os dados do briefing. Encerrando.")
        return None, None, None, None, None, None, None, None, None, None

    try:
        validate_briefing_data(brief_data)
    except ValueError as e:
        print(f"Erro de validação no briefing: {e}")
        return None, None, None, None, None, None, None, None, None, None

    nome_do_cliente = brief_data.get("nome_do_cliente", "")
    subnicho = brief_data.get("subnicho", "")
    informacoes_de_contato = brief_data.get("informacoes_de_contato", "")
    publico_alvo = brief_data.get("publico_alvo", "")
    tom_de_voz = brief_data.get("tom_de_voz", "")
    exemplos_de_nicho = brief_data.get("exemplos_de_nicho", [])
    tipo_de_conteudo = brief_data.get("tipo_de_conteudo", "")
    conteudos_semanais = brief_data.get("conteudos_semanais", [])
    objetivos_de_marketing = brief_data.get("objetivos_de_marketing", "")

    if not nome_do_cliente:
        print("Erro: 'nome_do_cliente' não encontrado no arquivo de briefing. Encerrando.")
        return None, None, None, None, None, None, None, None, None, None

    print(f"Briefing carregado para o cliente: {nome_do_cliente}")
    return brief_data, nome_do_cliente, subnicho, informacoes_de_contato, \
           publico_alvo, tom_de_voz, exemplos_de_nicho, tipo_de_conteudo, \
           conteudos_semanais, objetivos_de_marketing
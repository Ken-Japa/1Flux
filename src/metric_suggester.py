import json
import os

def suggest_metrics(campaign_type: str, objetivos_de_marketing: str) -> dict:
    """
    Sugere métricas de sucesso com base no tipo de campanha e objetivos de marketing.

    Args:
        campaign_type (str): O tipo de campanha (ex: "lancamento", "autoridade", "engajamento").
        objetivos_de_marketing (str): Uma descrição dos objetivos de marketing da campanha.

    Returns:
        dict: Um dicionário contendo as métricas de sucesso sugeridas, formatado para inclusão no JSON final.
    """
    script_dir = os.path.dirname(__file__)
    metricas_map_path = os.path.join(script_dir, "metricas_map.json")

    try:
        with open(metricas_map_path, 'r', encoding='utf-8') as f:
            metricas_map = json.load(f)
    except FileNotFoundError:
        print(f"Erro: O arquivo {metricas_map_path} não foi encontrado.")
        return {}
    except json.JSONDecodeError:
        print(f"Erro: O arquivo {metricas_map_path} não é um JSON válido.")
        return {}

    suggested_metrics = {
        "objetivo_principal": objetivos_de_marketing, # Usando a descrição completa como objetivo principal
        "indicadores_chave": [],
        "metricas_secundarias": []
    }

    if campaign_type in metricas_map:
        campaign_data = metricas_map[campaign_type]
        suggested_metrics["indicadores_chave"] = campaign_data.get("metricas_principais", [])
        suggested_metrics["metricas_secundarias"] = campaign_data.get("metricas_secundarias", [])
    else:
        print(f"Aviso: Tipo de campanha '{campaign_type}' não encontrado no metricas_map.json.")

    return suggested_metrics

if __name__ == '__main__':
    # Exemplo de uso
    campaign_type_example = "lancamento"
    objetivos_de_marketing_example = "Lançar a plataforma e gerar cadastros no trial gratuito"
    metrics = suggest_metrics(campaign_type_example, objetivos_de_marketing_example)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))

    campaign_type_example = "autoridade"
    objetivos_de_marketing_example = "Construir confiança e reputação no mercado"
    metrics = suggest_metrics(campaign_type_example, objetivos_de_marketing_example)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))

    campaign_type_example = "nao_existe"
    objetivos_de_marketing_example = "Um objetivo qualquer"
    metrics = suggest_metrics(campaign_type_example, objetivos_de_marketing_example)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
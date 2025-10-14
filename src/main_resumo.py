"""
Script principal para resumir os posts extraídos dos JSONs da Gemini e Cohere.
"""

import json
import os
import sys
from datetime import datetime

def find_latest_posts_file(directory):
    """
    Encontra o arquivo de posts mais recente em um diretório.
    
    Args:
        directory (str): Caminho do diretório a ser pesquisado
    
    Returns:
        str: Caminho completo do arquivo mais recente ou None se não encontrar
    """
    try:
        # Verificar se o diretório existe
        if not os.path.exists(directory):
            print(f"Diretório não encontrado: {directory}")
            return None
        
        # Listar todos os arquivos JSON no diretório
        files = [f for f in os.listdir(directory) if f.endswith('.json') and 'posts' in f]
        
        if not files:
            print(f"Nenhum arquivo de posts encontrado em: {directory}")
            return None
        
        # Ordenar por data de modificação (mais recente primeiro)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
        
        # Retornar o caminho completo do arquivo mais recente
        return os.path.join(directory, files[0])
    
    except Exception as e:
        print(f"Erro ao buscar arquivo mais recente: {str(e)}")
        return None

def load_posts_data(file_path):
    """
    Carrega os dados de posts de um arquivo JSON.
    
    Args:
        file_path (str): Caminho do arquivo JSON
    
    Returns:
        dict: Dados de posts carregados ou None se ocorrer um erro
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Erro ao carregar arquivo JSON: {str(e)}")
        return None

def save_summary(summary_data, ia_name, output_dir):
    """
    Salva o resumo dos posts em um arquivo JSON.
    
    Args:
        summary_data (dict): Dados do resumo a serem salvos
        ia_name (str): Nome da IA (Gemini ou Cohere)
        output_dir (str): Diretório onde o arquivo será salvo
    
    Returns:
        str: Caminho do arquivo salvo ou None se ocorrer um erro
    """
    try:
        # Criar diretório de saída se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        # Gerar nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{ia_name}_summary_{timestamp}.json"
        output_file_path = os.path.join(output_dir, output_filename)
        
        # Salvar o resumo em um novo arquivo
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(summary_data, file, ensure_ascii=False, indent=4)
        
        print(f"Resumo salvo com sucesso em: {output_file_path}")
        return output_file_path
    
    except Exception as e:
        print(f"Erro ao salvar resumo: {str(e)}")
        return None



def process_pre_summarized_file(ia_name, posts_dir, summary_output_dir):
    """
    Processa um arquivo de posts já resumido, carregando-o e salvando-o no diretório de resumo.
    
    Args:
        ia_name (str): Nome da IA (Gemini ou Cohere).
        posts_dir (str): Diretório onde os arquivos de posts resumidos estão localizados.
        summary_output_dir (str): Diretório onde o arquivo de resumo final será salvo.
    
    Returns:
        str: Caminho do arquivo de resumo salvo ou None se ocorrer um erro.
    """
    print(f"Processando arquivo de posts pré-resumido para {ia_name}...")
    
    # Encontrar o arquivo de posts mais recente
    posts_file_path = find_latest_posts_file(posts_dir)
    if not posts_file_path:
        print(f"Nenhum arquivo de posts encontrado para {ia_name} em {posts_dir}")
        return None
    
    # Carregar os dados de posts
    posts_data = load_posts_data(posts_file_path)
    if not posts_data:
        print(f"Falha ao carregar dados do arquivo {posts_file_path}")
        return None
    
    # Filtrar as propriedades de cada post
    filtered_posts = []
    for post in posts_data.get("posts", []):
        filtered_post = {
            "titulo": post.get("titulo"),
            "tema": post.get("tema"),
            "legenda_principal": post.get("legenda_principal"),
            "hashtags": post.get("hashtags", [])[:2], # Limitar a 2 hashtags
            "post_strategy_rationale": post.get("post_strategy_rationale"),
            "micro_briefing": post.get("micro_briefing") or post.get("carrossel_slides"), # Priorizar micro_briefing, senão usar carrossel_slides
            "cta_individual": post.get("cta_individual"),
            "interacao": post.get("interacao")
        }
        filtered_posts.append(filtered_post)
    
    # Criar um novo dicionário com os posts filtrados
    filtered_summary_data = {"posts": filtered_posts}

    # Salvar o resumo filtrado
    return save_summary(filtered_summary_data, ia_name, summary_output_dir)

def combine_summaries(gemini_summary_path, cohere_summary_path):
    """
    Combina os resumos da Gemini e Cohere em um único JSON.
    
    Args:
        gemini_summary_path (str): Caminho do arquivo de resumo da Gemini
        cohere_summary_path (str): Caminho do arquivo de resumo da Cohere
    
    Returns:
        str: Caminho do arquivo combinado ou None se ocorrer um erro
    """
    try:
        # Carregar os resumos
        gemini_data = load_posts_data(gemini_summary_path)
        cohere_data = load_posts_data(cohere_summary_path)
        
        if not gemini_data or not cohere_data:
            return None
        
        # Criar estrutura do JSON combinado
        combined_data = {
            "resumos": {
                "gemini": gemini_data.get("posts", []),
                "cohere": cohere_data.get("posts", [])
            }
        }
        
        # Criar diretório para o JSON combinado
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        combined_dir = os.path.join(base_dir, "output_files", "Resumo", "Enviar")
        os.makedirs(combined_dir, exist_ok=True)
        
        # Gerar nome do arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"combined_summary_{timestamp}.json"
        output_file_path = os.path.join(combined_dir, output_filename)
        
        # Salvar o JSON combinado
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(combined_data, file, ensure_ascii=False, indent=4)
        
        print(f"Resumo combinado salvo com sucesso em: {output_file_path}")
        return output_file_path
    
    except Exception as e:
        print(f"Erro ao combinar resumos: {str(e)}")
        return None



def main():
    """
    Função principal que processa os resumos da Gemini e Cohere.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Diretórios para Gemini
    gemini_posts_dir = os.path.join(base_dir, "output_files", "respostas_IA", "Gemini", "Resumo")
    gemini_summary_output_dir = os.path.join(base_dir, "output_files", "Resumo", "Gemini")

    # Diretórios para Cohere
    cohere_posts_dir = os.path.join(base_dir, "output_files", "respostas_IA", "Cohere", "Resumo")
    cohere_summary_output_dir = os.path.join(base_dir, "output_files", "Resumo", "Cohere")

    # Processar arquivo pré-resumido da Gemini
    gemini_summary_path = process_pre_summarized_file("Gemini", gemini_posts_dir, gemini_summary_output_dir)
    if gemini_summary_path:
        print(f"Resumo da Gemini processado com sucesso: {gemini_summary_path}")
    else:
        print("Falha ao processar resumo da Gemini")
        return

    # Processar arquivo pré-resumido da Cohere
    cohere_summary_path = process_pre_summarized_file("Cohere", cohere_posts_dir, cohere_summary_output_dir)
    if cohere_summary_path:
        print(f"Resumo da Cohere processado com sucesso: {cohere_summary_path}")
    else:
        print("Falha ao processar resumo da Cohere")
        return

    # Combinar os resumos em um único JSON
    combined_path = combine_summaries(gemini_summary_path, cohere_summary_path)
    if combined_path:
        print(f"Resumos combinados com sucesso: {combined_path}")
    else:
        print("Falha ao combinar resumos")

if __name__ == "__main__":
    main()
"""
Script principal para resumir os posts extraídos dos JSONs da Gemini e Cohere.
"""

import json
import os
import sys
from datetime import datetime
from src.utils.prompt_manager.build_summary_prompt import build_summary_prompt
from src.llm_client.gemini_client import generate_content as generate_gemini_content
from src.llm_client.cohere_client import generate_content as generate_cohere_content

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

def process_gemini_summary(posts_file_path=None):
    """
    Processa o resumo dos posts da Gemini.
    
    Args:
        posts_file_path (str, optional): Caminho do arquivo de posts. Se None, usa o mais recente.
    
    Returns:
        str: Caminho do arquivo de resumo salvo ou None se ocorrer um erro
    """
    # Diretórios
    base_dir = os.path.dirname(os.path.abspath(__file__))
    gemini_posts_dir = os.path.join(base_dir, "output_files", "respostas_IA", "Gemini", "Resumo")
    gemini_summary_dir = os.path.join(base_dir, "output_files", "Resumo", "Gemini")
    
    # Encontrar o arquivo de posts mais recente se não for especificado
    if not posts_file_path:
        posts_file_path = find_latest_posts_file(gemini_posts_dir)
        if not posts_file_path:
            return None
    
    # Carregar os dados de posts
    posts_data = load_posts_data(posts_file_path)
    if not posts_data:
        return None
    
    # Construir o prompt para resumo
    prompt = build_summary_prompt(posts_data, "Gemini")
    
    # Gerar o resumo usando a API da Gemini
    print("Gerando resumo com a Gemini...")
    summary_response = generate_gemini_content(prompt)
    
    # Processar a resposta para extrair o JSON
    try:
        # Tentar carregar diretamente como JSON
        summary_data = json.loads(summary_response)
    except json.JSONDecodeError:
        # Se falhar, tentar extrair o JSON da resposta de texto
        import re
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', summary_response)
        if json_match:
            try:
                summary_data = json.loads(json_match.group(1))
            except json.JSONDecodeError:
                print("Erro ao extrair JSON da resposta da Gemini")
                return None
        else:
            print("Formato de resposta da Gemini não reconhecido")
            return None
    
    # Salvar o resumo
    return save_summary(summary_data, "Gemini", gemini_summary_dir)

def process_cohere_summary(posts_file_path=None):
    """
    Processa o resumo dos posts da Cohere.
    
    Args:
        posts_file_path (str, optional): Caminho do arquivo de posts. Se None, usa o mais recente.
    
    Returns:
        str: Caminho do arquivo de resumo salvo ou None se ocorrer um erro
    """
    # Diretórios
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cohere_posts_dir = os.path.join(base_dir, "output_files", "respostas_IA", "Cohere", "Resumo")
    cohere_summary_dir = os.path.join(base_dir, "output_files", "Resumo", "Cohere")
    
    # Encontrar o arquivo de posts mais recente se não for especificado
    if not posts_file_path:
        posts_file_path = find_latest_posts_file(cohere_posts_dir)
        if not posts_file_path:
            return None
    
    # Carregar os dados de posts
    posts_data = load_posts_data(posts_file_path)
    if not posts_data:
        return None
    
    # Construir o prompt para resumo
    prompt = build_summary_prompt(posts_data, "Cohere")
    
    # Gerar o resumo usando a API da Cohere
    print("Gerando resumo com a Cohere...")
    summary_response = generate_cohere_content(prompt)
    
    # Processar a resposta para extrair o JSON
    try:
        # Tentar carregar diretamente como JSON
        summary_data = json.loads(summary_response)
    except json.JSONDecodeError:
        # Se falhar, tentar extrair o JSON da resposta de texto
        import re
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', summary_response)
        if json_match:
            try:
                summary_data = json.loads(json_match.group(1))
            except json.JSONDecodeError:
                print("Erro ao extrair JSON da resposta da Cohere")
                return None
        else:
            print("Formato de resposta da Cohere não reconhecido")
            return None
    
    # Salvar o resumo
    return save_summary(summary_data, "Cohere", cohere_summary_dir)

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
        base_dir = os.path.dirname(os.path.abspath(__file__))
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
    # Processar resumo da Gemini
    gemini_summary_path = process_gemini_summary()
    if gemini_summary_path:
        print(f"Resumo da Gemini gerado com sucesso: {gemini_summary_path}")
    else:
        print("Falha ao gerar resumo da Gemini")
        return
    
    # Processar resumo da Cohere
    cohere_summary_path = process_cohere_summary()
    if cohere_summary_path:
        print(f"Resumo da Cohere gerado com sucesso: {cohere_summary_path}")
    else:
        print("Falha ao gerar resumo da Cohere")
        return
    
    # Combinar os resumos em um único JSON
    combined_path = combine_summaries(gemini_summary_path, cohere_summary_path)
    if combined_path:
        print(f"Resumos combinados com sucesso: {combined_path}")
    else:
        print("Falha ao combinar resumos")

if __name__ == "__main__":
    main()
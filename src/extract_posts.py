import json
import os
import sys
from datetime import datetime

def extract_posts_from_json(input_file_path, output_dir):
    """
    Extrai apenas o array de posts de um arquivo JSON e salva em um novo arquivo.
    
    Args:
        input_file_path (str): Caminho para o arquivo JSON de entrada
        output_dir (str): Diretório onde o arquivo de saída será salvo
    
    Returns:
        str: Caminho do arquivo de saída criado ou None se ocorrer um erro
    """
    try:
        # Criar diretório de saída se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        # Ler o arquivo JSON de entrada
        with open(input_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Verificar se o campo 'posts' existe
        if 'posts' not in data:
            print(f"Erro: O campo 'posts' não foi encontrado no arquivo {input_file_path}")
            return None
        
        # Extrair apenas o array de posts
        posts_data = {"posts": data["posts"]}
        
        # Gerar nome do arquivo de saída com timestamp do arquivo original
        filename = os.path.basename(input_file_path)
        # Extrair o nome da IA (Gemini ou Cohere) do nome do arquivo
        if "Gemini" in filename:
            ia_name = "Gemini"
        elif "Cohere" in filename:
            ia_name = "Cohere"
        else:
            # Caso não seja possível identificar, usar o nome base do arquivo
            ia_name = os.path.splitext(filename)[0]
        
        # Extrair o timestamp do arquivo original (assumindo formato padrão)
        import re
        timestamp_match = re.search(r'(\d{8}_\d{6})', filename)
        if timestamp_match:
            timestamp = timestamp_match.group(1)
        else:
            # Se não encontrar o timestamp no nome do arquivo, usar o timestamp atual
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Criar o novo nome de arquivo no formato solicitado
        output_filename = f"{ia_name}_posts_{timestamp}.json"
        output_file_path = os.path.join(output_dir, output_filename)
        
        # Salvar o array de posts em um novo arquivo
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(posts_data, file, ensure_ascii=False, indent=4)
        
        print(f"Array de posts extraído com sucesso e salvo em: {output_file_path}")
        return output_file_path
    
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")
        return None

def main():
    """
    Função principal que processa os arquivos JSON da Gemini e Cohere.
    """
    # Diretório base
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_files_dir = os.path.join(base_dir, "output_files", "respostas_IA")
    
    # Diretórios de entrada e saída para Gemini
    gemini_input_dir = os.path.join(output_files_dir, "Gemini")
    gemini_output_dir = os.path.join(gemini_input_dir, "Resumo")
    
    # Diretórios de entrada e saída para Cohere
    cohere_input_dir = os.path.join(output_files_dir, "Cohere")
    cohere_output_dir = os.path.join(cohere_input_dir, "Resumo")
    
    # Processar arquivos da Gemini
    gemini_files = [f for f in os.listdir(gemini_input_dir) if f.endswith('.json') and os.path.isfile(os.path.join(gemini_input_dir, f))]
    if gemini_files:
        # Pegar o arquivo mais recente (ou você pode especificar um arquivo específico)
        gemini_file = gemini_files[-1]  # Assumindo que o último é o mais recente
        gemini_file_path = os.path.join(gemini_input_dir, gemini_file)
        print(f"Processando arquivo Gemini: {gemini_file_path}")
        extract_posts_from_json(gemini_file_path, gemini_output_dir)
    else:
        print("Nenhum arquivo JSON encontrado no diretório da Gemini.")
    
    # Processar arquivos da Cohere
    cohere_files = [f for f in os.listdir(cohere_input_dir) if f.endswith('.json') and os.path.isfile(os.path.join(cohere_input_dir, f))]
    if cohere_files:
        # Pegar o arquivo mais recente (ou você pode especificar um arquivo específico)
        cohere_file = cohere_files[-1]  # Assumindo que o último é o mais recente
        cohere_file_path = os.path.join(cohere_input_dir, cohere_file)
        print(f"Processando arquivo Cohere: {cohere_file_path}")
        extract_posts_from_json(cohere_file_path, cohere_output_dir)
    else:
        print("Nenhum arquivo JSON encontrado no diretório da Cohere.")

if __name__ == "__main__":
    main()
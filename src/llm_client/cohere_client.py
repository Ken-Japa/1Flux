import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
import cohere

load_dotenv()

def generate_text_content(prompt: str) -> dict:
    co = cohere.Client(os.getenv("COHERE_API_KEY"), timeout=600)
    try:
        response = co.chat(
            model="command-r-plus-08-2024",
            message=prompt,
            temperature=0.9  # Menor temperatura para respostas mais consistentes
        )
        # A Cohere retorna a resposta diretamente em response.text
        content = response.text.strip()

        # Extrair apenas o primeiro bloco JSON completo (incluindo chaves aninhadas)
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_string = json_match.group(0).strip()

            try:
                generated_content = json.loads(json_string)
                return {"status": "success", "generated_content": generated_content}
            except json.JSONDecodeError as e:
                # Se ainda falhar, salvar para depuração
                raw_responses_dir = os.path.join(os.path.dirname(__file__), 'raw_cohere_responses')
                os.makedirs(raw_responses_dir, exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = os.path.join(raw_responses_dir, f"mistral_raw_response_{timestamp}.txt")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                return {"status": "error", "message": f"JSON inválido após extração. Resposta salva em: {filename}. Erro: {e}"}
        else:
            return {"status": "error", "message": "Nenhum bloco JSON encontrado na resposta."}

    except Exception as e:
        return {"status": "error", "message": f"Erro ao gerar conteúdo: {e}"}

def generate_content(prompt: str) -> str:
    """
    Gera conteúdo de texto usando o modelo Cohere e retorna a resposta bruta.
    Função específica para o script de resumo de posts.

    Args:
        prompt (str): O prompt a ser enviado para o modelo.

    Returns:
        str: A resposta bruta do modelo.
    """
    co = cohere.Client(os.getenv("COHERE_API_KEY"), timeout=600)
    try:
        response = co.chat(
            model="command-r-plus-08-2024",
            message=prompt,
            temperature=0.9
        )
        return response.text.strip()
    except Exception as e:
        print(f"Erro ao gerar conteúdo com Cohere: {e}")
        return f"ERRO: {e}"

def generate_image_description(prompt: str) -> dict:
    co = cohere.Client(os.getenv("COHERE_API_KEY"), timeout=600)
    try:
        response = co.chat(
            model="command-r-plus-08-2024",
            message=prompt,
            temperature=0.9
        )
        # A Cohere retorna a resposta diretamente em response.text
        return {"status": "success", "visual_prompt": response.text}
    except Exception as e:
        return {"status": "error", "message": f"Erro ao gerar descrição de imagem: {e}"}

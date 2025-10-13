import os
import json
import re
import time
import google.generativeai as genai
import google.api_core.exceptions
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_text_content(prompt: str) -> dict:
    """
    Gera conteúdo de texto usando o modelo Gemini-Pro.

    Args:
        prompt (str): O prompt a ser enviado para o modelo.

    Returns:
        dict: Um dicionário contendo o conteúdo gerado ou uma mensagem de erro.
    """
    model = genai.GenerativeModel('gemini-2.5-pro')

    try:
        response = model.generate_content(str(prompt))
        try:
            json_string = re.sub(r"```json\n|```", "", response.text.strip())
            generated_content = json.loads(json_string)
            return {"status": "success", "generated_content": generated_content}
        except json.JSONDecodeError as e:
            return {"status": "error", "message": f"Erro de decodificação JSON na resposta da IA: {e}. Resposta bruta: {response.text}"}
    except google.api_core.exceptions.GoogleAPIError as e:
        return {"status": "error", "message": f"Falha na API Google Gemini: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Erro inesperado ao gerar conteúdo de texto: {e}"}

def generate_content(prompt: str) -> str:
    """
    Gera conteúdo de texto usando o modelo Gemini-Pro e retorna a resposta bruta.
    Função específica para o script de resumo de posts.

    Args:
        prompt (str): O prompt a ser enviado para o modelo.

    Returns:
        str: A resposta bruta do modelo.
    """
    model = genai.GenerativeModel('gemini-2.5-pro')

    try:
        response = model.generate_content(str(prompt))
        return response.text.strip()
    except google.api_core.exceptions.GoogleAPIError as e:
        print(f"Falha na API Google Gemini: {e}")
        return f"ERRO: {e}"
    except Exception as e:
        print(f"Erro inesperado ao gerar conteúdo: {e}")
        return f"ERRO: {e}"

def generate_image_description(prompt: str) -> dict:
    """
    Gera uma descrição de imagem/vídeo usando o modelo Gemini-Pro.

    Args:
        prompt (str): O prompt a ser enviado para o modelo.

    Returns:
        dict: Um dicionário contendo a descrição gerada ou uma mensagem de erro.
    """
    model = genai.GenerativeModel('gemini-pro')

    try:
        response = model.generate_content(prompt)
        return {"status": "success", "visual_prompt": response.text}
    except google.api_core.exceptions.GoogleAPIError as e:
        return {"status": "error", "message": f"Falha na API Google Gemini ao gerar descrição de imagem: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Erro inesperado ao gerar descrição de imagem: {e}"}
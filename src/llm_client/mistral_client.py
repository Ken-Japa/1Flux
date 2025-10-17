import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from mistralai import Mistral
import time

load_dotenv()

def generate_text_content(prompt: str) -> dict:
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"), timeout=300) # Aumentado timeout para 300 segundos (5 minutos)
    try:
        print(f"[{datetime.now()}] Chamando a API da Mistral para gerar conteúdo...")
        response = client.chat.complete(
            model="mistral-medium-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        print(f"[{datetime.now()}] Resposta da API da Mistral recebida. Iniciando processamento do conteúdo.")
        content = response.choices[0].message.content.strip()
        print(f"[{datetime.now()}] Conteúdo bruto da resposta da API (primeiros 500 caracteres): {content[:500]}...")

        # Tentar extrair o bloco JSON dentro de ```json ... ```
        print(f"[{datetime.now()}] Tentando extrair e parsear JSON da resposta...")
        json_match = re.search(r'```json\n([\s\S]*?)\n```', content, re.DOTALL)
        if json_match:
            json_string = json_match.group(1).strip()
            print(f"[{datetime.now()}] String JSON extraída (primeiros 500 caracteres): {json_string[:500]}...")
            try:
                generated_content = json.loads(json_string)
                print(f"[{datetime.now()}] JSON parseado com sucesso.")
                return {"status": "success", "generated_content": generated_content}
            except json.JSONDecodeError as e:
                print(f"[{datetime.now()}] Erro ao parsear JSON: {e}")
                # Se ainda falhar, salvar para depuração
                raw_responses_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'raw_mistral_responses')
                os.makedirs(raw_responses_dir, exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = os.path.join(raw_responses_dir, f"mistral_raw_response_{timestamp}.txt")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                return {"status": "error", "message": f"JSON inválido após extração. Resposta salva em: {filename}. Erro: {e}"}
        else:
            print(f"[{datetime.now()}] Nenhum bloco JSON encontrado na resposta.")
            return {"status": "error", "message": "Nenhum bloco JSON encontrado na resposta."}

    except Exception as e:
        print(f"[{datetime.now()}] Erro ao gerar conteúdo: {e}")
        return {"status": "error", "message": f"Erro ao gerar conteúdo: {e}"}

def generate_image_description(prompt: str) -> dict:
    """
    Gera uma descrição de imagem/vídeo usando o modelo da Mistral AI.
    Args:
        prompt (str): O prompt a ser enviado para o modelo.
    Returns:
        dict: Um dicionário contendo a descrição gerada ou uma mensagem de erro.
    """
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"), timeout=180) # Aumentado timeout para 180 segundos (3 minutos)
    try:
        print(f"[{datetime.now()}] Chamando a API da Mistral para gerar descrição de imagem...")
        response = client.chat.complete(
            model="mistral-medium-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        print(f"[{datetime.now()}] Resposta da API da Mistral para descrição de imagem recebida.")
        return {"status": "success", "visual_prompt": response.choices[0].message.content}
    except Exception as e:
        print(f"[{datetime.now()}] Erro ao gerar descrição de imagem: {e}")
        return {"status": "error", "message": f"Erro ao gerar descrição de imagem: {e}"}

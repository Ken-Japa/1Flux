import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

def generate_text_content(prompt: str) -> dict:
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    try:
        response = client.chat.complete(
            model="mistral-medium-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()

        # Extrair apenas o primeiro bloco JSON completo (incluindo chaves aninhadas)
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            json_string = json_match.group(0)
            # Corrigir possíveis quebras de linha ou formatação
            json_string = json_string.replace('\n', '').replace('\\"', '"')
            try:
                generated_content = json.loads(json_string)
                return {"status": "success", "generated_content": generated_content}
            except json.JSONDecodeError as e:
                # Se ainda falhar, salvar para depuração
                raw_responses_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'raw_mistral_responses')
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

def generate_image_description(prompt: str) -> dict:
    """
    Gera uma descrição de imagem/vídeo usando o modelo da Mistral AI.
    Args:
        prompt (str): O prompt a ser enviado para o modelo.
    Returns:
        dict: Um dicionário contendo a descrição gerada ou uma mensagem de erro.
    """
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    try:
        response = client.chat.complete(
            model="mistral-medium-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        return {"status": "success", "visual_prompt": response.choices[0].message.content}
    except Exception as e:
        return {"status": "error", "message": f"Erro ao gerar descrição de imagem: {e}"}

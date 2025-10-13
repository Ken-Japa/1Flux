import os
import json
from datetime import datetime
from src.config import BASE_DIR

def log_prompt(client_name: str, prompt: str, log_type: str = "content_generation"):
    """
    Salva o prompt utilizado em um arquivo de log para depuração.

    Args:
        client_name (str): Nome do cliente para identificar o log.
        prompt (str): O prompt completo enviado para a IA.
        log_type (str): Tipo de log (ex: "content_generation", "image_prompt").
    """
    log_dir = os.path.join(BASE_DIR, "src", "output_files", "logs_para_IA")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"prompt_log_{client_name.replace(' ', '_')}_{log_type}_{timestamp}.txt"
    filepath = os.path.join(log_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"--- Prompt Log ({log_type}) ---\n")
        f.write(f"Cliente: {client_name}\n")
        f.write(f"Data/Hora: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n")
        f.write("-------------------------------------\n\n")
        f.write(prompt)

    print(f"Prompt log salvo em: {filepath}")
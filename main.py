#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys

def run_script(module_name):
    """
    Executa um módulo Python usando subprocess.
    """
    print(f"\nExecutando: python -m {module_name}")
    try:
        # Usa sys.executable para garantir que o mesmo interpretador Python seja usado
        # Captura a saída para exibir no console
        result = subprocess.run([sys.executable, "-m", module_name], check=True, capture_output=True, text=True)
        print(f"Saída de {module_name}:\n{result.stdout}")
        if result.stderr:
            print(f"Erros de {module_name}:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {module_name}: {e}")
        print(f"Saída de erro: {e.stderr}")
    except FileNotFoundError:
        print(f"Erro: O interpretador Python não foi encontrado. Verifique sua instalação.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao executar {module_name}: {e}")

if __name__ == "__main__":
    print("Iniciando a execução sequencial dos scripts...")
    
    # Lista de módulos a serem executados em sequência
    modules_to_run = [
        "src.main_gemini",
        "src.main_cohere",
        "src.extract_posts",
        "src.main_resumo",
        "src.main_consolidar"
    ]

    for module in modules_to_run:
        run_script(module)
    
    print("\nExecução de todos os scripts concluída.")
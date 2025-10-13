#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

def clear_output_files(output_dir):
    """
    Apaga todos os arquivos dentro do diretório especificado e suas subpastas,
    mantendo a estrutura de diretórios intacta.
    """
    print(f"Iniciando a limpeza dos arquivos em: {output_dir}")
    if not os.path.exists(output_dir):
        print(f"O diretório de saída não existe: {output_dir}")
        return

    for root, dirs, files in os.walk(output_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Arquivo removido: {file_path}")
            except OSError as e:
                print(f"Erro ao remover o arquivo {file_path}: {e}")
    print("Limpeza de arquivos concluída.")

if __name__ == "__main__":
    # Define o diretório de saída a ser limpo
    # Certifique-se de que este caminho está correto para o seu ambiente
    output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_files")
    clear_output_files(output_directory)
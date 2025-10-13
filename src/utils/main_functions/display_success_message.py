import os

def display_success_message(output_pdf_filename, api_cost_usd):
    """
    Exibe uma mensagem de sucesso com os caminhos dos arquivos gerados e o custo estimado da API.

    Args:
        output_pdf_filename (str): O caminho completo do arquivo PDF gerado.
        api_cost_usd (float): O custo estimado da API em USD.
    """
    print("\n--- Processamento Concluído com Sucesso! ---")
    print(f"Caminho do PDF gerado: {os.path.abspath(output_pdf_filename)}")
    print(f"Custo estimado da API para esta geração: ${api_cost_usd:.4f}")
    print("------------------------------------------")
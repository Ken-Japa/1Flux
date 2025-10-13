import subprocess
import sys

def main():
    """
    Permite ao usuário escolher qual IA (Gemini, Mistral ou Cohere) executar
    e aciona o script principal correspondente no diretório 'src'.
    """
    while True:
        choice = input("Qual IA você quer utilizar? Use G [Gemini], M [Mistral] ou C [Cohere]: ").upper()

        if choice == 'G':
            script_to_run = 'src.main_gemini'
            break
        elif choice == 'M':
            script_to_run = 'src.main_mistral'
            break
        elif choice == 'C':
            script_to_run = 'src.main_cohere'
            break
        else:
            print("Escolha inválida. Por favor, digite G, M ou C.")

    print(f"Iniciando {script_to_run.split('.')[-1].replace('main_', '')}...")
    try:
        # Usa sys.executable para garantir que o mesmo interpretador Python seja usado
        # e -m para executar o módulo corretamente, independentemente de onde individual.py é chamado.
        subprocess.run([sys.executable, '-m', script_to_run], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script {script_to_run}: {e}")
    except FileNotFoundError:
        print(f"Erro: O interpretador Python não foi encontrado. Certifique-se de que o Python está no seu PATH.")

if __name__ == "__main__":
    main()
# Lógica dos Scripts Principais (src)

Este documento descreve a funcionalidade dos scripts Python localizados diretamente na pasta `src` do projeto `backend_concierge_scripts`. Ele oferece um resumo geral de cada arquivo e um detalhamento das funções contidas neles.

## Resumo Geral dos Arquivos

*   **`config.py`**: Contém configurações globais para a aplicação, como caminhos de diretório base, nome da empresa e caminho para o logo.
*   **`content_generator.py`**: Atua como um módulo agregador para funções relacionadas à geração de conteúdo, importando-as de submódulos em `utils/content_generator`.
*   **`data_storage.py`**: Serve como um módulo agregador para funções de interação com o banco de dados, importando-as de submódulos em `utils/data_storage`. Também inicializa o banco de dados e exporta briefings para JSON quando executado diretamente.
*   **`html_generator.py`**: Atua como um módulo agregador para funções relacionadas à geração de HTML, importando-as de submódulos em `utils/html_generator`.
*   **`main.py`**: É o ponto de entrada principal da aplicação. Orquestra o fluxo completo do Concierge MVP, desde a inicialização do ambiente e coleta de briefing até a geração de conteúdo, salvamento no banco de dados e criação de arquivos PDF e HTML.
*   **`pdf_generator.py`**: Atua como um módulo agregador para funções relacionadas à geração de PDF, importando-as de submódulos em `utils/pdf_generator`.
*   **`prompt_manager.py`**: Gerencia a construção e análise de prompts para modelos de linguagem (LLMs). Ele agrega funções de submódulos em `utils/prompt_manager` para construir prompts, analisar briefings e estimar o uso de tokens.

## Detalhamento das Funções por Arquivo

### `config.py`

Este arquivo define variáveis de configuração. Não contém funções executáveis diretamente, mas sim constantes.

*   **`BASE_DIR`**: Caminho absoluto para o diretório raiz do projeto.
*   **`COMPANY_NAME`**: Nome da empresa ("Fluxo Criativo").
*   **`LOGO_PATH`**: Caminho para o arquivo de logo da empresa.

### `content_generator.py`

Este arquivo importa funções de submódulos e as disponibiliza para uso.

*   **`generate_content_for_client`**: (Importada de `utils.content_generator.generate_content_for_client`) Responsável por gerar conteúdo para o cliente.
*   **`generate_image_prompts`**: (Importada de `utils.content_generator.generate_image_prompts`) Responsável por gerar prompts para criação de imagens.

### `data_storage.py`

Este arquivo importa funções de submódulos para gerenciar o armazenamento de dados.

*   **`init_db()`**: (Importada de `utils.data_storage.init_db`) Inicializa o banco de dados.
*   **`insert_brief(brief_data)`**: (Importada de `utils.data_storage.insert_brief`) Insere dados de um briefing no banco de dados.
*   **`get_briefs_by_client(client_name)`**: (Importada de `utils.data_storage.get_briefs_by_client`) Recupera briefings associados a um cliente específico.
*   **`insert_client_profile(profile_data)`**: (Importada de `utils.data_storage.insert_client_profile`) Insere ou atualiza o perfil de um cliente no banco de dados.
*   **`get_client_profile(client_name)`**: (Importada de `utils.data_storage.get_client_profile`) Recupera o perfil de um cliente.
*   **`get_all_briefs()`**: (Importada de `utils.data_storage.get_all_briefs`) Recupera todos os briefings do banco de dados.
*   **`update_brief_feedback(brief_id, feedback_data)`**: (Importada de `utils.data_storage.update_brief_feedback`) Atualiza o feedback de um briefing específico.
*   **`export_all_briefs_to_json()`**: (Importada de `utils.data_storage.export_all_briefs_to_json`) Exporta todos os briefings para um arquivo JSON.

### `html_generator.py`

Este arquivo importa funções de submódulos para gerar HTML.

*   **`create_briefing_html(content, client_name, output_dir)`**: (Importada de `utils.html_generator.create_briefing_html`) Cria um arquivo HTML com o briefing gerado.

### `main.py`

Este é o script principal que coordena todas as operações.

*   **`main()`**:
    *   **Descrição**: Orquestra o fluxo completo da aplicação.
    *   **Funcionalidade**:
        *   Inicializa o ambiente de trabalho (`initialize_environment`).
        *   Coleta e valida os dados do briefing do usuário (`collect_and_validate_briefing`).
        *   Obtém ou cria o perfil do cliente no banco de dados (`get_or_create_client_profile`).
        *   Gera o conteúdo de mídia social com base no briefing (`generate_social_media_content`).
        *   Salva o conteúdo gerado e os detalhes da geração no banco de dados (`save_content_to_database`).
        *   Gera um arquivo PDF do briefing (`generate_briefing_pdf`).
        *   Gera um arquivo HTML do briefing (`generate_briefing_html`).
        *   Exibe uma mensagem de sucesso ao usuário (`display_success_message`).

### `pdf_generator.py`

Este arquivo importa funções de submódulos para gerar PDFs.

*   **`create_briefing_pdf(content, client_name, output_dir)`**: (Importada de `utils.pdf_generator.create_briefing_pdf`) Cria um arquivo PDF com o briefing gerado.

### `prompt_manager.py`

Este arquivo gerencia a criação e análise de prompts para LLMs.

*   **`PromptManager` (Classe)**:
    *   **`__init__()`**: Inicializa a classe `PromptManager`.
    *   **`build_prompt(client_profile, niche_guidelines, content_type, weekly_themes, weekly_goal, strategic_analysis=None)`**:
        *   **Descrição**: Constrói o prompt completo para a API do Gemini.
        *   **Retorna**: O prompt completo formatado como string.
    *   **`analyze_briefing_for_strategy(client_profile, niche_guidelines=None)`**:
        *   **Descrição**: Analisa o briefing do cliente para extrair informações estratégicas.
        *   **Retorna**: Um dicionário com informações estratégicas analisadas.
    *   **`build_image_prompt(client_profile, post_content)`**:
        *   **Descrição**: Constrói um prompt detalhado para uma IA de geração de imagens/vídeos.
        *   **Retorna**: O prompt visual detalhado como string.
    *   **`get_token_count(prompt_text)`**:
        *   **Descrição**: Estima o número de tokens de um prompt (baseado no número de palavras).
        *   **Retorna**: O número estimado de tokens como um inteiro.
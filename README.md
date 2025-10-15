# MVP Concierge - Resumo do Progresso

Este documento resume as principais atividades e desenvolvimentos realizados no projeto `mvp_concierge`.

Popular o client_briefing.json com os dados do cliente.
Roda o processo todo (gemini - cohere - resumo - mistral consolidado)
python main.py
Limpa os arquivos na pasta output_files
python clear.py
Escolhe qual IA rodar individualmente
python individual.py

Renderização Separada
python generate_pdf_from_json.py "output_files/respostas_IA/Gemini/Gemini_content_json_debug_20251013_204310.json"
python generate_html_from_json.py "output_files/respostas_IA/Consolidado/mistral_response_InvestFacil_20251015_084841.json"

## Visão Geral do Projeto

O projeto `mvp_concierge` é composto por três módulos principais:

- `backend_concierge_scripts`: Contém a lógica de backend para geração de conteúdo, gerenciamento de prompts e armazenamento de dados.
- `data_validation_concierge`: Destinado à validação de dados, utilizando arquivos de referência.
- `landing_page_concierge`: Responsável pela página de destino.

## Progresso e Modificações Recentes

### 1. Armazenamento de Dados (`db.sqlite`)

- **Objetivo**: Garantir que o banco de dados `db.sqlite` seja criado e os dados sejam armazenados corretamente.
- **Implementação**: Modificações em `src/data_storage.py` para:
  - Utilizar um caminho absoluto para o `db.sqlite` (`backend_concierge_scripts/src/data/db.sqlite`).
  - Assegurar a criação do diretório `data` se ele não existir.
  - Adição de mensagens de depuração para rastrear a criação do diretório e do banco de dados.
- **Status**: O arquivo `db.sqlite` agora é criado no local esperado. A verificação do conteúdo dos dados está pendente.

### 2. Prevenção de Sobrescrita de Arquivos

- **Objetivo**: Evitar que arquivos PDF e HTML gerados sejam sobrescritos em execuções consecutivas do script.
- **Implementação**: Modificações em `src/main.py` para:
  - Incluir um carimbo de data/hora detalhado (com horas e minutos) nos nomes dos arquivos PDF e HTML gerados.

### 3. Clarificação dos Arquivos de Entrada e Referência

- **`client_briefing.json`**: Confirmado como o arquivo de entrada manual para cada execução do script, contendo os dados do cliente para processamento.
- **`client_briefs.csv` e `client_profiles.json` (em `data_validation_concierge`)**: Esclarecido que estes são arquivos de dados de referência pré-existentes, não populados manualmente a cada execução, e que o script os utiliza para validação ou como base de conhecimento, mas não os gera ou os usa para popular o `db.sqlite` no fluxo atual.

### 4. Verificação de Dados no Banco de Dados

- **Implementação**: Adicionada uma função temporária `get_all_briefs()` em `src/data_storage.py` e sua chamada em `src/main.py` para recuperar e imprimir todos os briefings de clientes após a inserção dos dados, a fim de verificar o armazenamento correto.
- **Status**: Aguardando execução para verificar a saída e confirmar o armazenamento dos dados.

### 5. Duplicata de Mistral

Main
content_generator
generate_social_media_content (main functions)
generate_content_for_client (content generator)
generate_image_prompts (content generator)

"mistral-small-latest" ou "mistral-medium-latest" ou "mistral-large-latest"

### 6. Cohere

models : "command-r-08-2024" ou "command-r-plus-08-2024"

Precisa-se definir o local do arquivo json em main_cohere

### Script de resumo

Precisa-se definir o local do arquivo json para ser resumido

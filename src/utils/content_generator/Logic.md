# Lógica do content_generator.py

O arquivo `content_generator.py` serve como o ponto de entrada principal para a geração de conteúdo na aplicação. Ele atua como um orquestrador, importando e utilizando as funções refatoradas de `generate_content_for_client` e `generate_image_prompts`.

## Visão Geral do content_generator.py

Este arquivo centraliza a lógica de chamada das funções de geração de conteúdo, gerenciando o fluxo de trabalho completo. Sua principal responsabilidade é integrar os diferentes módulos (geração de conteúdo textual, geração de prompts de imagem, gerenciamento de cache e gerenciamento de prompts) para fornecer uma interface unificada para a criação de conteúdo.

## Funções Principais e Suas Lógicas

### `generate_content_for_client`

**Localização:** `generate_content_for_client.py`

**Propósito:** Responsável por gerar conteúdo textual detalhado para clientes, utilizando a API do Google Gemini. Esta função lida com a complexidade de construir prompts, interagir com a LLM e processar suas respostas.

**Lógica Detalhada:**
1.  **Construção da Chave de Cache:** Uma chave única é gerada com base nos parâmetros de entrada (`client_profile`, `content_type`, `weekly_themes`, `weekly_goal`) para identificar se uma solicitação semelhante já foi processada.
2.  **Verificação de Cache:** Antes de qualquer processamento, a função verifica se o resultado já existe no cache. Se sim, o resultado é retornado instantaneamente, otimizando o desempenho e reduzindo custos.
3.  **Inicialização do PromptManager:** Uma instância de `PromptManager` é criada com o `client_profile` para gerenciar a construção de prompts específicos para o cliente.
4.  **Análise Estratégica:** O `PromptManager` é utilizado para realizar uma análise estratégica inicial do briefing do cliente, o que ajuda a refinar o prompt principal.
5.  **Construção do Prompt:** O prompt final para a LLM é construído dinamicamente, incorporando o tipo de conteúdo, temas semanais, objetivo semanal e a análise estratégica.
6.  **Estimativa de Tokens e Custo:** Antes de enviar para a LLM, a função estima o número de tokens do prompt e o custo associado, fornecendo transparência sobre o consumo de recursos.
7.  **Chamada à API Gemini com Retentativas:** A função tenta chamar a API `generate_text_content` (do `gemini_client`) para obter o conteúdo. Em caso de falha, um mecanismo de retentativa com backoff exponencial é implementado para lidar com erros transitórios da API.
8.  **Processamento da Resposta da LLM:**
    *   A resposta bruta da LLM é analisada para extrair um objeto JSON. A função tenta identificar o JSON dentro de blocos de código Markdown (` ```json `) ou, como fallback, procura por uma estrutura JSON bruta.
    *   É realizada uma validação básica da estrutura JSON esperada (ex: verificar a existência de chaves importantes como `weekly_strategy_summary`).
9.  **Armazenamento em Cache:** Se a geração de conteúdo for bem-sucedida, o resultado é armazenado no cache para futuras solicitações.
10. **Retorno do Resultado:** Um dicionário contendo o status, o conteúdo gerado, o prompt enviado e o uso de tokens/custo é retornado.

**Dependências:**
*   `PromptManager`: Para construção e gerenciamento de prompts.
*   `cache_manager`: Para operações de cache (get, set, key generation).
*   `gemini_client`: Para interagir com a API do Google Gemini (`generate_text_content`).

### `generate_image_prompts`

**Localização:** `generate_image_prompts.py`

**Propósito:** Gera um prompt descritivo otimizado para IAs de geração de imagens/vídeos, com base no conteúdo de um post e no perfil do cliente.

**Lógica Detalhada:**
1.  **Inicialização do PromptManager:** Uma instância de `PromptManager` é criada para auxiliar na construção do prompt visual.
2.  **Construção do Prompt Visual:** O `PromptManager` é utilizado para construir um prompt específico para a geração de imagens, levando em consideração o `post_content` e o `client_profile`.
3.  **Estimativa de Tokens e Custo:** Similar à função de geração de conteúdo textual, estima-se o uso de tokens e o custo.
4.  **Chamada à API Gemini:** A função chama a API `generate_image_description` (do `gemini_client`) para obter a descrição visual.
5.  **Processamento e Retorno:** A resposta da API é processada, e o prompt visual gerado é retornado junto com o status e informações de uso de tokens/custo.

**Dependências:**
*   `PromptManager`: Para construção de prompts visuais.
*   `gemini_client`: Para interagir com a API do Google Gemini (`generate_image_description`).

## Informações Relevantes Adicionais

*   **Modularidade:** A refatoração resultou em uma arquitetura modular, onde cada responsabilidade (geração de conteúdo textual, geração de prompts de imagem, gerenciamento de prompts, gerenciamento de cache, interação com LLM) é encapsulada em seu próprio módulo. Isso facilita a manutenção, teste e escalabilidade do sistema.
*   **Otimização de Desempenho e Custo:** A implementação de um sistema de cache reduz significativamente o número de chamadas redundantes à API da LLM, resultando em melhor desempenho e menor custo operacional.
*   **Tratamento de Erros:** Mecanismos robustos de tratamento de erros, incluindo retentativas e validação de respostas, garantem a resiliência do sistema contra falhas da API ou respostas inesperadas.
*   **Flexibilidade:** A arquitetura permite fácil extensão para suportar novos tipos de conteúdo, diferentes modelos de LLM ou estratégias de cache, com impacto mínimo no código existente.
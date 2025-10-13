# Lógica do Módulo PromptManager

## Resumo Executivo

O módulo `PromptManager` é a espinha dorsal da estratégia de geração de conteúdo, atuando como um orquestrador central para a criação e gestão de prompts otimizados para Modelos de Linguagem Grandes (LLMs), como o Google Gemini. Sua arquitetura modular, com funções auxiliares refatoradas em arquivos separados, garante um código limpo, manutenível e escalável. Ele centraliza a interface para todas as operações relacionadas a prompts, delegando a execução de lógicas específicas para módulos menores e especializados, facilitando a adaptação e expansão futuras.

## Lógica Geral do `prompt_manager.py`

O arquivo `prompt_manager.py` define a classe `PromptManager`, que serve como uma interface unificada para interagir com as diversas funcionalidades de construção e análise de prompts. Em vez de conter a lógica de implementação diretamente, a classe `PromptManager` importa e expõe funções de módulos auxiliares localizados no diretório `utils/prompt_manager`. Essa abordagem promove:

*   **Modularidade**: Cada função auxiliar é responsável por uma tarefa específica, tornando o código mais fácil de entender, testar e manter.
*   **Reusabilidade**: As funções auxiliares podem ser utilizadas independentemente, se necessário, ou integradas em outros contextos.
*   **Organização**: A separação de responsabilidades evita que o arquivo principal se torne excessivamente grande e complexo.

A classe `PromptManager` não mantém estado interno significativo, atuando principalmente como um "proxy" para as funções auxiliares. Isso simplifica seu uso e reduz a chance de efeitos colaterais indesejados.

## Detalhamento das Funções Auxiliares

### 1. `analyze_briefing_for_strategy.py`

**Função:** `analyze_briefing_for_strategy(briefing_content: str) -> dict`

**Lógica:**
Esta função é responsável por processar o conteúdo bruto de um briefing do cliente e extrair informações estratégicas cruciais. A implementação atual utiliza uma abordagem baseada em palavras-chave e padrões de texto para identificar elementos como:

*   **Objetivos Estratégicos**: O que o cliente deseja alcançar com o conteúdo.
*   **Público-Alvo Detalhado**: Características demográficas e psicográficas do público.
*   **Tom de Voz**: A personalidade e o estilo de comunicação desejados.
*   **Palavras-Chave**: Termos relevantes para SEO e relevância do conteúdo.
*   **Referências de Estilo**: Exemplos de conteúdo que o cliente aprecia ou deseja emular.
*   **Canais de Distribuição**: Onde o conteúdo será publicado (ex: Instagram, Facebook, Blog).
*   **Restrições Legais**: Quaisquer limitações ou requisitos legais.
*   **Orçamento Disponível**: Informações sobre o investimento.
*   **Cronograma Desejado**: Prazos para a entrega do conteúdo.
*   **Métricas de Sucesso**: Como o sucesso do conteúdo será medido.
*   **Informações Adicionais**: Qualquer outro dado relevante.

A função itera sobre o `briefing_content` (convertido para minúsculas para facilitar a busca) e procura por marcadores específicos (ex: "objetivos:", "público-alvo:"). Uma vez encontrado um marcador, ela extrai o texto subsequente até a próxima quebra de linha ou o final do briefing.

**Importância:** Esta análise inicial é fundamental para contextualizar a geração de prompts, garantindo que o conteúdo gerado esteja alinhado com as necessidades e expectativas do cliente.

### 2. `build_image_prompt.py`

**Função:** `build_image_prompt(client_profile: dict, post_content: dict) -> str`

**Lógica:**
Esta função constrói um prompt textual detalhado, especificamente formatado para ser utilizado por IAs de geração de imagens ou vídeos (como Midjourney, DALL-E, Stable Diffusion). Ela combina informações do perfil do cliente com detalhes do conteúdo do post para criar uma descrição visual rica e precisa.

Os principais elementos considerados são:

*   **Nome do Cliente, Subnicho, Tom de Voz, Público-Alvo**: Para contextualizar a imagem/vídeo com a marca.
*   **Legenda Principal do Post (`main_caption`)**: O texto que a imagem/vídeo deve complementar.
*   **Formato Sugerido (`suggested_format`)**: Indica se é uma imagem, vídeo curto, carrossel, etc.

A função estrutura o prompt visual com instruções claras sobre:

*   **Cenário e Ambiente**: Onde a cena se passa.
*   **Elementos Visuais Principais**: O que deve aparecer na imagem/vídeo.
*   **Estilo Artístico**: A estética desejada (realista, cartoon, etc.).
*   **Cores e Iluminação**: A paleta de cores e o tipo de luz.
*   **Emoções e Atmosfera**: O sentimento que a imagem deve evocar.
*   **Composição e Enquadramento**: Como a cena deve ser "fotografada".
*   **Texto/Sobreposição**: Se houver texto na imagem.

**Importância:** Garante que as representações visuais geradas pela IA sejam coesas com o conteúdo textual e a identidade da marca do cliente, otimizando a comunicação visual.

### 3. `build_prompt.py`

**Função:** `build_prompt(client_profile: dict, niche_guidelines: dict, content_type: str, weekly_themes: list[str], weekly_goal: str, strategic_analysis: dict = None) -> str`

**Lógica:**
Esta é a função central para a construção do prompt completo que será enviado ao LLM (Google Gemini). Ela agrega uma vasta quantidade de informações de diferentes fontes para criar uma instrução abrangente e altamente contextualizada para a geração de conteúdo.

Os dados são coletados e combinados de:

*   **`client_profile`**: Detalhes sobre o cliente, incluindo nome, subnicho, tom de voz, público-alvo, objetivos de marketing, exemplos de nicho, canais de distribuição, tópicos principais, palavras-chave, CTA, restrições, informações adicionais, referências de concorrentes e estilo.
*   **`niche_guidelines`**: Diretrizes específicas do nicho que podem complementar ou refinar as informações do perfil do cliente.
*   **`content_type`**: O tipo específico de conteúdo a ser gerado (ex: 'instagram_post', 'blog_post').
*   **`weekly_themes`**: Uma lista de temas que devem ser abordados na semana.
*   **`weekly_goal`**: O objetivo principal da campanha de conteúdo para a semana.
*   **`strategic_analysis`**: O resultado da análise do briefing, fornecendo insights estratégicos adicionais.

A função constrói o prompt em duas partes principais:

*   **`system_message`**: Define o papel do LLM (ex: "Você é um copywriter especializado em mídias sociais para [subnicho]").
*   **`user_message`**: Contém todas as instruções detalhadas para a geração do conteúdo, incluindo:
    *   **Perfil do Cliente**: Informações básicas e avançadas.
    *   **Análise Estratégica Inicial**: Contexto do subnicho, análise de concorrentes e informações adicionais.
    *   **Informações Estratégicas do Briefing**: Dados extraídos pela função `analyze_briefing_for_strategy`.
    *   **Contexto Semanal**: Temas e objetivos da semana.
    *   **Instruções de Formato**: Detalhes sobre a estrutura da campanha (5 posts com narrativa progressiva), o que cada post deve conter (título, legenda, variações, hashtags, formato sugerido, justificativa estratégica, micro-briefing, micro-roteiro, slides de carrossel, sugestão de prompt visual).
    *   **Formato de Saída JSON**: Uma estrutura JSON detalhada que o LLM deve seguir para retornar o conteúdo.

**Importância:** Esta função é crucial para garantir que o LLM receba todas as informações necessárias e instruções claras para gerar conteúdo de alta qualidade, relevante e estruturado conforme as necessidades do cliente.

### 4. `get_token_count.py`

**Função:** `get_token_count(prompt_text: str) -> int`

**Lógica:**
Esta função fornece uma estimativa simples do número de tokens em um determinado texto de prompt. Atualmente, a implementação utiliza uma contagem de palavras como proxy para a contagem de tokens (`len(prompt_text.split())`).

**Considerações:**
*   **Estimativa vs. Precisão**: É importante notar que esta é uma estimativa. A contagem exata de tokens depende do tokenizador específico utilizado pelo modelo de LLM (ex: Google Gemini usa seu próprio tokenizador). Uma contagem de palavras é uma aproximação razoável para muitos casos, mas pode não ser totalmente precisa para limites rigorosos de tokens.
*   **Melhorias Futuras**: Para maior precisão, seria necessário integrar um tokenizador específico do modelo (se disponível publicamente via SDK) ou uma biblioteca que simule essa tokenização.

**Importância:** Ajuda a gerenciar os limites de tokens das APIs de LLMs, prevenindo erros de estouro de limite e otimizando o custo das chamadas à API.
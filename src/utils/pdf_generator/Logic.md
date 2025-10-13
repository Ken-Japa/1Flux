# Lógica do Módulo `pdf_generator`

## Resumo Geral

O módulo `pdf_generator` é responsável por transformar dados estruturados (geralmente em formato JSON) em um "PDF de Briefing Profissional" visualmente atraente e bem organizado. Ele atua como um orquestrador, utilizando diversas funções auxiliares para construir cada seção do documento, garantindo modularidade e fácil manutenção. O arquivo principal, `create_briefing_pdf.py`, coordena a criação do PDF, desde a definição de estilos até a inclusão de capa, sumário executivo, seções de posts, calendário e checklist de publicação, além de cabeçalhos e rodapés consistentes.

## Detalhamento das Funções

### `create_briefing_pdf` (no arquivo `create_briefing_pdf.py`)

*   **Propósito:** Esta é a função principal do módulo. Ela recebe os dados do briefing em formato JSON, o nome do cliente, o período e o nome do arquivo de saída, e gera o PDF completo.
*   **Lógica:**
    1.  **Inicialização de Estilos:** Obtém os estilos padrão do ReportLab e adiciona uma série de estilos personalizados (como `TitleStyle`, `SubtitleStyle`, `SectionTitle`, `NormalText`, `PostTitle`, etc.) para garantir a consistência visual do documento.
    2.  **Criação do Documento:** Instancia um objeto `SimpleDocTemplate` do ReportLab, configurando o nome do arquivo de saída e o tamanho da página (carta).
    3.  **Construção da "Story":** A "story" é uma lista de elementos que compõem o conteúdo do PDF. A função `create_briefing_pdf` chama as funções auxiliares para adicionar cada seção à "story":
        *   `_build_cover_page`: Adiciona a página de capa.
        *   `_build_executive_summary`: Adiciona o sumário executivo.
        *   Loop para `_build_post_section`: Itera sobre cada post no JSON de conteúdo e adiciona uma seção detalhada para cada um.
        *   `_build_publication_calendar`: Adiciona o calendário de publicação sugerido.
        *   `_build_publication_checklist`: Adiciona o checklist de publicação.
    4.  **Construção Final do PDF:** Chama o método `doc.build()` para gerar o PDF. Durante este processo, as funções `_header_footer` são aplicadas para adicionar cabeçalhos e rodapés em todas as páginas.

### `_build_cover_page` (no arquivo `_build_cover_page.py`)

*   **Propósito:** Constrói e retorna os elementos da página de capa do PDF.
*   **Lógica:**
    1.  **Elementos Estáticos:** Adiciona parágrafos com o título do documento, nome do cliente, período e nome da empresa, utilizando os estilos definidos.
    2.  **Inclusão de Logo:** Verifica se o `LOGO_PATH` (definido em `config.py`) existe. Se sim, carrega a imagem, ajusta seu tamanho para caber na página e a centraliza. Em caso de erro ou logo não encontrado, adiciona um placeholder de texto.
    3.  **Data de Geração:** Inclui a data atual de geração do PDF.
    4.  **Separador:** Adiciona uma linha horizontal (`HRFlowable`) para separar visualmente as informações.

### `_build_executive_summary` (no arquivo `_build_executive_summary.py`)

*   **Propósito:** Constrói e retorna os elementos da seção de sumário executivo.
*   **Lógica:**
    1.  **Quebra de Página:** Inicia uma nova página e define um novo template de página (`NormalPage`).
    2.  **Título da Seção:** Adiciona o título "Sumário Executivo" com o estilo `SectionTitle`.
    3.  **Conteúdo do Sumário:** Adiciona parágrafos para o resumo da estratégia semanal, objetivos (listados individualmente), público-alvo e tom de voz, extraindo os dados do dicionário `weekly_strategy_summary` e aplicando os estilos apropriados (`SummaryTitle`, `SummaryText`).

### `_build_post_section` (no arquivo `_build_post_section.py`)

*   **Propósito:** Constrói e retorna os elementos para um post individual dentro da seção de "Ideias de Conteúdo".
*   **Lógica:**
    1.  **Título do Post:** Adiciona o título do post, incluindo seu número e o título principal, com o estilo `PostTitle`.
    2.  **Detalhes do Post:** Para cada campo do post (justificativa estratégica, legenda principal, variações de legenda, hashtags, sugestão de formato, sugestões visuais detalhadas), adiciona um subtítulo (`PostSubtitle`) e o conteúdo correspondente (`PostText`, `PostHashtag`, `PostFormat`, `PostVisuals`). As variações de legenda e hashtags são formatadas adequadamente.

### `_build_publication_calendar` (no arquivo `_build_publication_calendar.py`)

*   **Propósito:** Constrói e retorna os elementos da seção de calendário de publicação sugerido.
*   **Lógica:**
    1.  **Quebra de Página:** Inicia uma nova página e define um novo template de página (`NormalPage`).
    2.  **Título da Seção:** Adiciona o título "Calendário de Publicação Sugerido" com o estilo `SectionTitle`.
    3.  **Listagem de Entradas:** Itera sobre a lista `publication_calendar`. Para cada dia, adiciona o nome do dia (`CalendarTitle`) e, em seguida, lista as entradas de publicação para aquele dia, incluindo hora e conteúdo (`CalendarEntry`). Se não houver calendário, exibe uma mensagem.

### `_build_publication_checklist` (no arquivo `_build_publication_checklist.py`)

*   **Propósito:** Constrói e retorna os elementos da seção de checklist de publicação.
*   **Lógica:**
    1.  **Quebra de Página:** Inicia uma nova página e define um novo template de página (`NormalPage`).
    2.  **Título da Seção:** Adiciona o título "Checklist de Publicação" com o estilo `SectionTitle`.
    3.  **Listagem de Itens:** Itera sobre a lista `publication_checklist`. Para cada item, adiciona um parágrafo formatado como item de checklist (`ChecklistItem`). Se não houver checklist, exibe uma mensagem.

### `_header_footer` (no arquivo `_header_footer.py`)

*   **Propósito:** Esta função é um callback utilizada pelo ReportLab para adicionar cabeçalhos e rodapés a cada página do PDF.
*   **Lógica:**
    1.  **Estado do Canvas:** Salva o estado atual do canvas para garantir que as alterações feitas para o rodapé não afetem o conteúdo principal da página.
    2.  **Rodapé:** Define a fonte, tamanho e cor do texto. Constrói o texto do rodapé, que inclui o `COMPANY_NAME` (importado de `config.py`) e o número da página atual. Centraliza o texto do rodapé na parte inferior da página.
    3.  **Restauração do Canvas:** Restaura o estado anterior do canvas.

## Informações Relevantes Adicionais

*   **`config.py`:** Este arquivo é crucial para a configuração global do gerador de PDF. Ele define constantes como `COMPANY_NAME` e `LOGO_PATH`, que são utilizadas por várias funções para personalizar o PDF. A utilização de um arquivo de configuração centralizado facilita a gestão de variáveis que podem mudar entre diferentes implantações ou clientes.
*   **ReportLab:** A biblioteca ReportLab é a base para a geração do PDF. Ela oferece um controle granular sobre a formatação, posicionamento de elementos, estilos e estrutura do documento. A abordagem de "story" (lista de elementos de fluxo) é fundamental para construir o conteúdo de forma programática.
*   **Modularidade:** A divisão do gerador de PDF em funções auxiliares (`_build_...`) promove a modularidade do código. Cada função é responsável por uma parte específica do documento, tornando o código mais legível, testável e fácil de manter. Isso também permite a reutilização de componentes em outros contextos, se necessário.
*   **Estilos:** A definição de estilos personalizados no `create_briefing_pdf` centraliza a gestão da aparência do PDF. Isso garante que todos os elementos visuais (títulos, textos, etc.) sigam um padrão consistente em todo o documento.
*   **Tratamento de Erros (Logo):** A função `_build_cover_page` inclui um tratamento básico de erros para o carregamento do logo, exibindo um placeholder caso o arquivo não seja encontrado ou ocorra um erro durante o carregamento.
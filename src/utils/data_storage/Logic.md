# Lógica do `data_storage.py` e Módulos de Armazenamento de Dados

O arquivo `data_storage.py` atua como o ponto de entrada e orquestrador principal para todas as operações de armazenamento e recuperação de dados relacionadas aos briefings e perfis de clientes. Ele foi refatorado para promover a modularidade e a clareza, delegando as responsabilidades específicas de banco de dados a módulos dedicados dentro do pacote `mvp_concierge.backend_concierge_scripts.src.utils.data_storage`.

## Estrutura e Propósito Geral:

-   **Ponto de Entrada Centralizado**: `data_storage.py` é o script principal que coordena as interações com o banco de dados. Ao invés de implementar a lógica de banco de dados diretamente, ele importa e expõe as funções de outros módulos, tornando-o um hub para as operações de dados.
-   **Modularização Eficaz**: Cada operação CRUD (Create, Read, Update, Delete) e outras funcionalidades de dados foram encapsuladas em arquivos Python separados. Isso melhora a organização do código, facilita a manutenção, o teste e a reutilização de componentes individuais.
-   **Configuração Unificada**: As configurações essenciais do banco de dados, como o caminho do arquivo SQLite, são centralizadas em `database_config.py`, garantindo consistência e fácil modificação.
-   **Importações Robustas**: O uso de importações absolutas em `data_storage.py` e importações relativas dentro do pacote `data_storage` garante que as funções sejam acessíveis corretamente, independentemente do contexto de execução.
-   **Exemplo de Uso (`if __name__ == '__main__':`)**: O bloco de execução condicional demonstra um fluxo de trabalho típico, como a inicialização do banco de dados e a exportação de dados, servindo como um exemplo prático de como as funções modularizadas podem ser utilizadas.

Esta refatoração visa criar uma arquitetura de dados mais robusta, escalável e fácil de entender, onde cada componente tem uma responsabilidade clara.

## Detalhamento das Funções e Lógica dos Módulos:

### `database_config.py`
-   **Propósito**: Define configurações globais relacionadas ao banco de dados.
-   **Lógica**:
    -   Importa `sqlite3`, `json`, `os` e `datetime`. Embora `json` e `datetime` não sejam usados diretamente neste arquivo, eles são comumente usados em outros módulos que interagem com o banco de dados, e sua inclusão aqui pode ser para fins de consistência ou para evitar imports repetidos em outros lugares (embora seja mais comum importar onde são usados).
    -   `DATABASE_PATH`: Constrói o caminho absoluto para o arquivo `db.sqlite` dentro de um diretório `data`. Utiliza `os.path.dirname(os.path.abspath(__file__))` para garantir que o caminho seja sempre relativo à localização do script, tornando-o portátil.

### `init_db.py`
-   **Propósito**: Inicializa o banco de dados SQLite, criando as tabelas necessárias se elas ainda não existirem.
-   **Lógica**:
    -   Importa `sqlite3` para interagir com o banco de dados e `os` para manipulação de diretórios.
    -   Importa `DATABASE_PATH` de `database_config.py`.
    -   A função `init_db()`:
        -   Garante a existência do diretório `data` onde o arquivo `db.sqlite` será armazenado, usando `os.makedirs(DATA_DIR, exist_ok=True)`.
        -   Estabelece uma conexão com o banco de dados usando `sqlite3.connect(DATABASE_PATH)`.
        -   Cria a tabela `client_briefs` com colunas para `id`, `client_name`, `subniche`, `brief_data` (JSON string), `generated_content` (JSON string), `prompt_used`, `tokens_consumed`, `api_cost_usd`, `delivery_date` e `feedback_summary`.
        -   Cria a tabela `client_profiles` com colunas para `id`, `client_name` (UNIQUE), `contact_info`, `public_target`, `tone_of_voice`, `niche_examples` (JSON string) e `status`.
        -   Utiliza `CREATE TABLE IF NOT EXISTS` para evitar erros se as tabelas já existirem.
        -   Confirma as alterações (`conn.commit()`) e fecha a conexão (`conn.close()`).

### `insert_brief.py`
-   **Propósito**: Insere um novo registro de briefing no banco de dados.
-   **Lógica**:
    -   Importa `sqlite3`, `json` (para serializar dados complexos) e `datetime` (para a data de entrega padrão).
    -   Importa `DATABASE_PATH`.
    -   A função `insert_brief()`:
        -   Recebe vários parâmetros que descrevem um briefing.
        -   Define `delivery_date` como a data atual se não for fornecida.
        -   Conecta-se ao banco de dados.
        -   Serializa `brief_data` e `generated_content` para strings JSON usando `json.dumps()` antes de inseri-los.
        -   Executa uma instrução `INSERT` na tabela `client_briefs`.
        -   Confirma e fecha a conexão.

### `get_briefs_by_client.py`
-   **Propósito**: Recupera todos os briefings associados a um cliente específico.
-   **Lógica**:
    -   Importa `sqlite3` e `json` (para desserializar dados complexos).
    -   Importa `DATABASE_PATH`.
    -   A função `get_briefs_by_client()`:
        -   Recebe o `client_name` como parâmetro.
        -   Conecta-se ao banco de dados.
        -   Executa uma instrução `SELECT *` na tabela `client_briefs` filtrando pelo `client_name`.
        -   Recupera todas as linhas correspondentes (`cursor.fetchall()`).
        -   Para cada linha, desserializa `brief_data` e `generated_content` de strings JSON para objetos Python usando `json.loads()`.
        -   Retorna uma lista de dicionários, onde cada dicionário representa um briefing.

### `insert_client_profile.py`
-   **Propósito**: Insere ou atualiza o perfil de um cliente no banco de dados.
-   **Lógica**:
    -   Importa `sqlite3` e `json` (para serializar `niche_examples`).
    -   Importa `DATABASE_PATH`.
    -   A função `insert_client_profile()`:
        -   Recebe os detalhes do perfil do cliente.
        -   Conecta-se ao banco de dados.
        -   Serializa `niche_examples` para uma string JSON.
        -   Executa uma instrução `INSERT OR REPLACE` na tabela `client_profiles`. Isso significa que se um perfil com o mesmo `client_name` já existir, ele será atualizado; caso contrário, um novo será inserido.
        -   Confirma e fecha a conexão.

### `get_client_profile.py`
-   **Propósito**: Recupera o perfil de um cliente específico.
-   **Lógica**:
    -   Importa `sqlite3` e `json` (para desserializar `niche_examples`).
    -   Importa `DATABASE_PATH`.
    -   A função `get_client_profile()`:
        -   Recebe o `client_name`.
        -   Conecta-se ao banco de dados.
        -   Executa um `SELECT *` na tabela `client_profiles` filtrando pelo `client_name`.
        -   Recupera a primeira linha correspondente (`cursor.fetchone()`).
        -   Se um perfil for encontrado, desserializa `niche_examples` e retorna o perfil como um dicionário.
        -   Retorna `None` se nenhum perfil for encontrado.

### `get_all_briefs.py`
-   **Propósito**: Recupera todos os briefings de todos os clientes no banco de dados.
-   **Lógica**:
    -   Importa `sqlite3` e `json` (para desserializar dados).
    -   Importa `DATABASE_PATH`.
    -   A função `get_all_briefs()`:
        -   Conecta-se ao banco de dados.
        -   Executa um `SELECT *` na tabela `client_briefs` sem filtros.
        -   Recupera todas as linhas.
        -   Para cada linha, desserializa `brief_data` e `generated_content` e os adiciona a uma lista de dicionários.
        -   Retorna a lista completa de briefings.

### `update_brief_feedback.py`
-   **Propósito**: Atualiza o campo `feedback_summary` de um briefing específico.
-   **Lógica**:
    -   Importa `sqlite3`.
    -   Importa `DATABASE_PATH`.
    -   A função `update_brief_feedback()`:
        -   Recebe o `brief_id` e o `feedback_summary`.
        -   Conecta-se ao banco de dados.
        -   Executa uma instrução `UPDATE` na tabela `client_briefs` para definir o `feedback_summary` para o `brief_id` fornecido.
        -   Confirma e fecha a conexão.

### `export_all_briefs_to_json.py`
-   **Propósito**: Exporta todos os briefings do banco de dados para um arquivo JSON.
-   **Lógica**:
    -   Importa `json` e `os`.
    -   Importa a função `get_all_briefs` do módulo correspondente.
    -   A função `export_all_briefs_to_json()`:
        -   Chama `get_all_briefs()` para obter todos os briefings.
        -   Define o diretório de saída (`output_dir`) de forma relativa ao script, garantindo que seja criado em `output_files/dados_clientes`.
        -   Cria o diretório de saída se ele não existir (`os.makedirs(output_dir, exist_ok=True)`).
        -   Salva a lista de briefings em um arquivo JSON formatado (`indent=4`, `ensure_ascii=False`) no caminho especificado.

### `__init__.py`
-   **Propósito**: Transforma o diretório `data_storage` em um pacote Python e define quais módulos e funções são expostos quando o pacote é importado.
-   **Lógica**:
    -   Contém instruções `from .module_name import function_name` para cada função pública dos módulos dentro do pacote. Isso permite que `data_storage.py` (ou qualquer outro script) importe diretamente as funções do pacote `data_storage` como se fossem membros diretos do pacote, por exemplo, `from mvp_concierge.backend_concierge_scripts.src.utils.data_storage import init_db`.

## Considerações Adicionais:

-   **Tratamento de Erros**: Embora as funções atuais incluam `try-except` básicos para criação de diretórios, uma implementação mais robusta incluiria tratamento de exceções para operações de banco de dados (e.g., `sqlite3.Error`) para lidar com falhas de conexão, erros de consulta, etc.
-   **Fechamento de Conexões**: É crucial garantir que as conexões com o banco de dados sejam sempre fechadas. O uso de `with sqlite3.connect(...) as conn:` pode simplificar isso, garantindo que a conexão seja fechada automaticamente, mesmo em caso de erros.
-   **Validação de Dados**: Para aplicações de produção, seria importante adicionar validação de dados nos parâmetros de entrada das funções para garantir a integridade dos dados antes de inseri-los no banco de dados.
-   **Segurança**: Para evitar ataques de injeção SQL, todas as consultas utilizam parâmetros (`?`) em vez de formatação de string direta, o que é uma boa prática de segurança.
# Guia para Criação de Prompt a partir do client_briefing.json

Este guia detalha como cada campo do `client_briefing.json` deve ser utilizado na construção do prompt para a IA, indicando sua obrigatoriedade, opcionalidade e impacto na geração de conteúdo.

## Estrutura do client_briefing.json (Referência)

```json
{
  "nome_do_cliente": "",
  "subnicho": "",
  "informacoes_de_contato": "",
  "publico_alvo": "",
  "tom_de_voz": "",
  "exemplos_de_nicho": [],
  "objetivos_de_marketing": "",
  "canais_de_distribuicao": [],
  "topicos_principais": [],
  "palavras_chave": [],
  "chamada_para_acao": "",
   "restricoes_e_diretrizes": "",
  "informacoes_adicionais": "",
  "referencias_de_concorrentes": [],
  "referencias_de_estilo_e_formato": [],
  "tipo_de_conteudo": "",
  "conteudos_semanais": []
}
```

## Detalhamento dos Campos para o Prompt

### `nome_do_cliente`
*   **Obrigatório**: Sim.
*   **Impacto no Prompt**: Essencial para personalizar a saudação e o contexto inicial do prompt, garantindo que a IA se refira ao cliente corretamente e adapte o tone de voz.
*   **Uso no Prompt**: "Você está criando conteúdo para [nome_do_cliente]..."

### `subnicho`
*   **Obrigatório**: Sim.
*   **Impacto no Prompt**: Crucial para direcionar a IA a um segmento específico, garantindo que o conteúdo seja altamente relevante e focado.
*   **Uso no Prompt**: "...que atua no subnicho de [subnicho]..."

### `informacoes_de_contato`
*   **Obrigatório**: Não (Opcional).
*   **Impacto no Prompt**: Não afeta diretamente o prompt da IA, mas pode ser incluído para referência interna ou em relatórios.
*   **Uso no Prompt**: Não aplicável diretamente ao prompt de geração de conteúdo.

### `publico_alvo`
*   **Obrigatório**: Sim.
*   **Impacto no Prompt**: Fundamental para a IA adaptar a linguagem, o tom e os temas ao público desejado, garantindo que a mensagem seja eficaz.
*   **Uso no Prompt**: "O público-alvo é [publico_alvo]..."

### `tom_de_voz`
*   **Obrigatório**: Sim.
*   **Impacto no Prompt**: Guia a IA na escolha da linguagem, personalidade e estilo de comunicação, garantindo a consistência da marca.
*   **Uso no Prompt**: "O tom de voz deve ser [tom_de_voz]..."

### `exemplos_de_nicho`
*   **Obrigatório**: Não (Opcional).
*   **Impacto no Prompt**: Fornece à IA exemplos concretos de conteúdo ou estilo que o cliente aprecia, ajudando a refinar a geração.
*   **Uso no Prompt**: "Considere os seguintes exemplos de nicho para inspiração: [exemplos_de_nicho]..."

### `objetivos_de_marketing`
*   **Obrigatório**: Sim.
*   **Impacto no Prompt**: Guia a IA na criação de conteúdo focado em metas específicas (ex: aumentar vendas, engajamento, reconhecimento de marca).
*   **Uso no Prompt**: "Os objetivos de marketing são [objetivos_de_marketing]..."

### `canais_de_distribuicao`
*   **Obrigatório**: Sim.
*   **Impacto no Prompt**: Influencia o formato, a extensão e o estilo do conteúdo, permitindo que a IA adapte a saída para cada canal (ex: post para redes sociais, artigo para blog, script para vídeo).
*   **Uso no Prompt**: "O conteúdo será distribuído nos seguintes canais: [canais_de_distribuicao]..."

### `topicos_principais`
*   **Obrigatório**: Sim.
*   **Impacto no Prompt**: Define os temas gerais que o conteúdo deve abordar, ajudando a IA a manter o foco nos assuntos centrais e a gerar conteúdo relevante.
*   **Uso no Prompt**: "Os tópicos principais a serem abordados são: [topicos_principais]..."

### `palavras_chave`
*   **Obrigatório**: Sim.
*   **Impacto no Prompt**: Essencial para otimização SEO e para garantir que o conteúdo gerado seja relevante para as buscas do público-alvo.
*   **Uso no Prompt**: "Inclua as seguintes palavras-chave no conteúdo: [palavras_chave]..."

### `chamada_para_acao`
*   **Obrigatório**: Não (Opcional).
*   **Impacto no Prompt**: Se fornecida, a IA incorporará a CTA no conteúdo, direcionando o leitor para a próxima ação desejada.
*   **Uso no Prompt**: "A chamada para ação é: [chamada_para_acao]..."

### `restricoes_e_diretrizes`
*   **Obrigatório**: Não (Opcional, mas altamente recomendado).
*   **Impacto no Prompt**: Guia a IA sobre o que evitar, garantindo que o conteúdo esteja alinhado com as políticas da marca e as sensibilidades do público.
*   **Uso no Prompt**: "Considere as seguintes restrições e diretrizes: [restricoes_e_diretrizes]..."

### `informacoes_adicionais`
*   **Obrigatório**: Não (Opcional).
*   **Impacto no Prompt**: Permite incluir qualquer informação extra que possa ser útil para a IA, mas que não se encaixa em outros campos, oferecendo contexto adicional.
*   **Uso no Prompt**: "Informações adicionais a serem consideradas: [informacoes_adicionais]..."

### `referencias_de_concorrentes`
*   **Obrigatório**: Não (Opcional).
*   **Impacto no Prompt**: Ajuda a IA a entender o cenário competitivo e a diferenciar o conteúdo gerado, evitando similaridades e buscando originalidade.
*   **Uso no Prompt**: "Analise o conteúdo dos seguintes concorrentes para inspiração e diferenciação: [referencias_de_concorrentes]..."

### `referencias_de_estilo_e_formato`
*   **Obrigatório**: Não (Opcional, mas altamente recomendado).
*   **Impacto no Prompt**: Ajuda a IA a replicar um estilo visual e de formatação específico, garantindo a coesão com a identidade da marca.
*   **Uso no Prompt**: "Considere as seguintes referências de estilo e formato: [referencias_de_estilo_e_formato]..."

### `tipo_de_conteudo`
*   **Obrigatório**: Sim.
*   **Impacto no Prompt**: Crítico para informar a IA sobre os formatos de conteúdo esperados em um nível macro (ex: blog post, e-mail marketing, roteiro de vídeo).
*   **Uso no Prompt**: "O tipo de conteúdo a ser gerado é: [tipo_de_conteudo]..."

### `conteudos_semanais`
*   **Obrigatório**: Não (Opcional).
*   **Impacto no Prompt**: Permite à IA entender a estrutura e os requisitos de cada conteúdo individual dentro de um plano semanal, incluindo chamadas para ação e objetivos específicos.
*   **Uso no Prompt**: "Para cada conteúdo semanal, considere:
    *   **`chamada_para_acao_individual`**: [chamada_para_acao_individual] (Opcional)
    *   **`objetivo_do_conteudo_individual`**: [objetivo_do_conteudo_individual] (Opcional)
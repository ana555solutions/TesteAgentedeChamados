# Roteiro da Apresentação

## 1. Abertura — 1 minuto

"Vou apresentar uma solução de tratamento automatizado de chamados usando IA, regras determinísticas e RPA.

O fluxo recebe o chamado, interpreta os dados com IA, decide se a solicitação pode ser automatizada e, quando autorizada, executa a automação. Casos ambíguos ou de risco são enviados para revisão humana."

## 2. Arquitetura — 2 minutos

Mostrar o `ARCHITECTURE.md` ou explicar visualmente:

Chamado → Agente de IA → Motor de Decisão → Automação/Revisão Humana → Resultado/Evidência → Atualização do chamado.

Destacar que a IA não executa diretamente a ação. A decisão final passa pelo motor de regras.

## 3. IA — 2 minutos

Abrir o Swagger e mostrar um chamado.

Executar o processamento e mostrar:

- classificação;
- dados extraídos;
- atividade;
- confiança;
- decisão;
- justificativa.

Mostrar rapidamente que a resposta é estruturada e validada pelo Pydantic.

## 4. Caso Web — 2 minutos

Usar o ticket `01_web_sucesso`.

Mostrar:

1. criação do chamado;
2. processamento;
3. decisão de automação;
4. execução do Playwright;
5. evidência gerada;
6. status concluído.

Abrir o screenshot em `evidence/`.

## 5. Caso Desktop — 2 minutos

Usar o ticket `02_desktop_sucesso`.

Mostrar a Calculadora do Windows sendo utilizada pelo pywinauto.

Resultado esperado: `10 + 5 = 15`.

Mostrar a evidência gerada.

## 6. Casos que NÃO devem ser automatizados — 3 minutos

Mostrar os três casos obrigatórios:

### Inconsistência

`03_inconsistencia`

CH-123 é o alvo, mas os dados pertencem ao CH-456.

Resultado: revisão humana.

### Ação em massa

`04_acao_em_massa`

Fechar todos os chamados de uma área.

Resultado: revisão humana.

### Dados faltantes

`05_dados_faltantes`

Não existe número do chamado nem nova prioridade.

Resultado: revisão humana.

## 7. Falha do RPA — 2 minutos

Usar `09_falha_rpa_web`.

Explicar:

"Mesmo que a IA autorize a automação, a execução pode falhar. Nesse caso o sistema registra a falha, marca o chamado como falho e cria uma nova entrada na fila humana."

Mostrar o log e a fila.

## 8. Logs e evidências — 1 minuto

Abrir:

- `logs/automation.log`
- pasta `evidence/`
- endpoint `/tickets/queues`

Mostrar que existe rastreabilidade da decisão e da execução.

## 9. Encerramento — 1 minuto

"Como evolução para produção, eu adicionaria autenticação e autorização, banco gerenciado, observabilidade centralizada, métricas, auditoria e controle de versões dos prompts e modelos.

A arquitetura atual já separa interpretação da IA, decisão determinística e execução RPA, permitindo adicionar essas camadas sem alterar o fluxo principal."

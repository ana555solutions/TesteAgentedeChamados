# Arquitetura e Decisões Técnicas

## 1. Objetivo

A solução implementa um fluxo de tratamento automatizado de chamados utilizando um agente de IA, regras de decisão e automações RPA.

O fluxo completo é:

1. Recebimento do chamado
2. Análise pelo agente de IA
3. Extração das informações relevantes
4. Avaliação da decisão por regras determinísticas
5. Encaminhamento para automação ou revisão humana
6. Execução da automação RPA, quando aplicável
7. Registro do resultado e das evidências
8. Atualização do chamado

A IA é responsável por interpretar o chamado, mas a execução da automação é controlada por regras determinísticas.

---

## 2. Arquitetura

```text
                 ┌─────────────────────┐
                 │     Chamado         │
                 │   Ticket / API      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Agente de IA     │
                 │                     │
                 │ Classificação       │
                 │ Extração de dados   │
                 │ Atividade           │
                 │ Confiança           │
                 │ Risco               │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Motor de Decisão    │
                 │                     │
                 │ Confiança >= 80%    │
                 │ Consistência        │
                 │ Risco               │
                 │ Escopo              │
                 │ Dados obrigatórios  │
                 └──────────┬──────────┘
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
        ┌─────────────────┐   ┌─────────────────┐
        │   Automação     │   │ Revisão Humana  │
        │                 │   │                 │
        │ Playwright      │   │ Fila humana     │
        │ pywinauto       │   │ Motivo          │
        └────────┬────────┘   └─────────────────┘
                 │
                 ▼
        ┌─────────────────────┐
        │ Resultado + Evidência│
        │ + Logs               │
        └──────────┬──────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Atualização do  │
          │ chamado         │
          └─────────────────┘

3. Principais componentes

FastAPI
Responsável pela API do sistema de chamados.

Endpoints principais:

POST /tickets — cria um chamado
GET /tickets — lista chamados
GET /tickets/{ticket_id} — consulta um chamado
PATCH /tickets/{ticket_id} — atualiza um chamado
POST /tickets/{ticket_id}/process — processa um chamado
GET /tickets/queues — consulta as filas de automação e revisão humana
Agente de IA

O agente utiliza um modelo de linguagem local através do Ollama.

Responsabilidades:

Classificar o chamado
Resumir a solicitação
Extrair dados relevantes
Identificar a atividade solicitada
Identificar informações ausentes
Identificar inconsistências
Avaliar risco
Informar nível de confiança
Sugerir automação ou revisão humana

A resposta do agente é estruturada em JSON e validada através de modelos Pydantic.

Motor de Decisão

O motor de decisão aplica regras determinísticas após a análise da IA.
O limite de confiança definido é:
80%

A automação não é liberada quando:

A confiança está abaixo de 80%
Existe inconsistência entre os dados
A atividade apresenta alto risco
A solicitação possui escopo amplo
Existem dados obrigatórios ausentes
A execução da automação falha

Dessa forma, a IA não possui controle direto sobre a execução da automação.

Processador de Chamados

O processador coordena todo o fluxo:
Chamado
   ↓
Agente de IA
   ↓
Motor de decisão
   ↓
Automação ou revisão humana
   ↓
Resultado
   ↓
Atualização do chamado

Também é responsável por registrar logs e tratar exceções.

4. Fluxo de decisão

O processo segue as seguintes etapas:

O agente analisa o chamado.
Os dados extraídos são validados.
O motor de decisão verifica a confiança.
São verificadas inconsistências.
É avaliado o risco da atividade.
É avaliado o escopo da solicitação.
São verificadas informações obrigatórias.
Se os critérios forem atendidos, a automação é liberada.
Caso contrário, o chamado é enviado para revisão humana.

O objetivo é evitar que uma interpretação incorreta da IA resulte diretamente em uma alteração no sistema.

5. Revisão humana

Quando a automação não é autorizada, o chamado recebe:
status = revisao_humana

Também é criada uma entrada na fila:
queue_type = human_review
status = pending

O motivo do encaminhamento é armazenado junto à fila.

Exemplos:

Confiança abaixo do limite
Inconsistência entre chamados
Dados obrigatórios ausentes
Atividade de alto risco
Solicitação com escopo amplo

Os dados extraídos pela IA permanecem disponíveis para auxiliar o tratamento humano.

6. Tratamento de falhas

Falhas durante a execução da automação são tratadas através de try/except.

Quando uma automação falha:

A falha é registrada no log.
O chamado recebe status falhou.
O resultado registra a mensagem de erro.
A execução da automação é marcada como failed.
Um novo item é criado na fila de revisão humana.

Dessa forma, uma falha do robô não fica sem tratamento.

7. Evidências

Cada automação gera evidências da execução.

RPA Web
Utiliza Playwright e gera um screenshot da página após a execução.

Exemplo:

evidence/CH-012_browser.png
RPA Desktop

Utiliza pywinauto para executar uma operação na Calculadora do Windows e captura a tela do resultado.

Exemplo:
evidence/desktop_calculator.png

As evidências são armazenadas no chamado.

8. Logs

O sistema possui logging centralizado em:

logs/automation.log

Os logs registram informações como:

Início do processamento
Decisão da IA
Nível de confiança
Encaminhamento para revisão humana
Início da automação
Tipo de RPA executado
Sucesso da automação
Falhas
Encaminhamento para revisão após falha

Informações desnecessárias ou dados sensíveis do chamado não são intencionalmente registrados nos logs.

9. Persistência de dados

A solução utiliza SQLite com SQLAlchemy.

As principais informações armazenadas são:

Chamados
Identificador
Descrição
Categoria
Prioridade
Área solicitante
Resumo
Dados extraídos
Decisão
Confiança
Justificativa
Status
Resultado
Evidências
Datas de criação e atualização
Fila
Chamado
Tipo da fila
Status
Motivo
Data de criação
Data de processamento

10. Decisões técnicas

Python
Escolhido como linguagem principal por permitir integrar facilmente:

API
IA
Banco de dados
Automação Web
Automação Desktop
Logging
FastAPI

Utilizado para disponibilizar a API do sistema e facilitar a execução e demonstração através do Swagger.

Ollama
Utilizado para executar o modelo de IA localmente, sem necessidade de uma chave de API externa.

Pydantic
Utilizado para garantir que a resposta do agente siga uma estrutura definida.

Playwright
Utilizado para automação Web.

pywinauto
Utilizado para automação Desktop no Windows.

SQLite
Utilizado como banco de dados local para manter a solução simples e reproduzível durante a demonstração.

11. Segurança e produção

Para uma implementação em produção, alguns pontos poderiam ser aprimorados:

Utilização de banco de dados gerenciado
Autenticação e autorização da API
Gerenciamento seguro de credenciais
Monitoramento centralizado
Métricas de execução
Controle de versões dos prompts
Avaliação contínua da qualidade da IA
Auditoria das decisões
Controle de acesso às filas humanas
Retentativas controladas para falhas transitórias
Integração com o sistema real de chamados

As credenciais e configurações sensíveis devem permanecer fora do código-fonte.

12. Estrutura do projeto
automation-pro/
│
├── app/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── prompts.py
│   │   └── schemas.py
│   │
│   ├── rpa/
│   │   ├── browser.py
│   │   └── desktop.py
│   │
│   ├── routes/
│   │   └── tickets.py
│   │
│   ├── services/
│   │   ├── decision.py
│   │   └── ticket_service.py
│   │
│   ├── database.py
│   ├── database_models.py
│   ├── logging_config.py
│   ├── models.py
│   ├── main.py
│   └── ticket_processor.py
│
├── evidence/
├── logs/
├── mock_web/
├── tests/
│
├── .env
├── .env.example
├── .gitignore
├── ARCHITECTURE.md
├── README.md
└── requirements.txt
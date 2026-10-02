# Automation Pro

Agente de IA e RPA para tratamento automatizado de chamados.

## Descrição

Projeto desenvolvido em Python para análise de chamados utilizando um agente de IA, tomada de decisão baseada em regras determinísticas e execução de atividades através de RPA.

O sistema recebe um chamado, interpreta sua solicitação, extrai os dados necessários, avalia riscos e consistência e decide entre automação ou revisão humana.

Fluxo principal:

```text
Ticket
   ↓
Agente de IA
   ↓
Extração estruturada
   ↓
Motor de decisão
   ↓
┌─────────────────────┐
│                     │
Automação       Revisão humana
│                     │
RPA                   Fila humana
│
Resultado + evidência
│
Atualização do ticket

## Índice

- [Descrição](#descrição)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Executar a API](#executar-a-api)
- [Banco de dados](#banco-de-dados)
- [Agente de IA](#agente-de-ia)
- [Motor de decisão](#motor-de-decisão)
- [RPA Web](#rpa-web)
- [RPA Desktop](#rpa-desktop)
- [Evidências](#evidências)
- [Tratamento de falhas](#tratamento-de-falhas)
- [Fila de processamento](#fila-de-processamento)
- [Fluxo pelo Swagger](#fluxo-pelo-swagger)
- [Casos de validação](#casos-de-validação)
- [Testes](#testes)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Logs](#logs)
- [Segurança](#segurança)
- [Decisões técnicas](#decisões-técnicas)

## Arquitetura

                    ┌─────────────────────┐
                    │      FastAPI        │
                    │   API de Tickets    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Ticket Processor   │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
        ┌─────────────────┐         ┌─────────────────┐
        │    AI Agent     │         │ Decision Engine │
        │    Ollama       │         │  Regras fixas   │
        └────────┬────────┘         └────────┬────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Automação aprovada? │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
        ┌─────────────────┐         ┌─────────────────┐
        │   Web RPA       │         │  Desktop RPA    │
        │   Playwright    │         │    pywinauto    │
        └────────┬────────┘         └────────┬────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                    Resultado + evidência
                               │
                               ▼
                       Atualização ticket

Tecnologias
Python
FastAPI
SQLite
SQLAlchemy
Pydantic
Ollama
gpt-oss:20b
Playwright
pywinauto
HTTP/REST
Requisitos
Python 3.11+
Ollama instalado
Modelo gpt-oss:20b
Windows, necessário para a automação desktop com pywinauto
Instalação

Clone o projeto e entre na pasta:

cd automation-pro

Crie o ambiente virtual:

python -m venv .venv

Ative:

.venv\Scripts\activate

Instale as dependências:

pip install -r requirements.txt

Instale os navegadores do Playwright:

playwright install

Confirme que o Ollama está funcionando:

ollama list

O modelo utilizado pelo projeto é:

gpt-oss:20b

Caso ainda não esteja instalado:

ollama pull gpt-oss:20b
Executar a API

Com o ambiente virtual ativado:

uvicorn app.main:app --reload

API:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health
Banco de dados

O projeto utiliza SQLite.

O arquivo:

automation_pro.db

é criado automaticamente na primeira execução da aplicação.

As principais entidades são:

Tickets
Queue Items

A tabela de fila registra tanto execuções de automação quanto encaminhamentos para revisão humana.

Agente de IA

O agente utiliza o modelo gpt-oss:20b através do Ollama.

A análise retorna uma estrutura validada pelo Pydantic contendo:

classificação
resumo
dados extraídos
atividade solicitada
decisão sugerida
confiança
justificativa
campos faltantes
risco

Entre os dados extraídos estão:

número do chamado alvo
número do chamado relacionado aos dados
prioridade solicitada
área solicitante
resultado solicitado
números utilizados em operações matemáticas
outros dados relevantes

O agente não executa diretamente as automações. A decisão final de liberar a execução passa pelo motor de decisão determinístico.

Motor de decisão

O limite de confiança utilizado atualmente é:

80%

A automação é bloqueada quando:

a confiança está abaixo do limite;
existe inconsistência entre chamado alvo e chamado dos dados;
a atividade é classificada como de alto risco;
a solicitação possui escopo amplo ou em massa;
faltam dados essenciais;
os dados necessários para a atividade não estão disponíveis.

Quando a execução não é liberada, o chamado recebe:

status = revisao_humana

e uma entrada é criada na fila de revisão humana.

RPA Web

A automação Web utiliza Playwright.

O projeto possui uma aplicação web local em:

mock_web/index.html

A automação executa uma atualização de prioridade de chamado.

São realizadas as seguintes etapas:

Abrir a aplicação.
Informar o número do chamado.
Selecionar a nova prioridade.
Executar a atualização.
Ler o resultado exibido.
Capturar screenshot como evidência.

Teste:

python test_browser_rpa.py
RPA Desktop

A automação Desktop utiliza pywinauto no Windows.

O cenário implementado utiliza a Calculadora do Windows.

Exemplo:

10 + 5

O robô:

Abre a Calculadora.
Digita o primeiro número.
Executa a operação.
Digita o segundo número.
Executa o cálculo.
Lê o resultado real exibido pela aplicação.
Captura screenshot da execução.
Retorna resultado e evidência.
Evidências

As evidências das execuções são armazenadas em:

evidence/

Exemplos:

evidence/
├── CH-123_browser.png
└── desktop_calculator.png

As evidências são associadas ao ticket após a execução.

Tratamento de falhas

Falhas durante a execução do RPA são tratadas pelo Ticket Processor.

Quando uma automação falha:

status do ticket → falhou

A execução de automação é registrada como:

queue_type → automation
status → failed

E uma nova entrada é criada automaticamente:

queue_type → human_review
status → pending

Dessa forma, uma falha técnica não resulta em uma execução silenciosamente perdida.

Fila de processamento

A fila pode ser consultada através de:

GET /tickets/queues

Os itens possuem informações como:

ticket_id
tipo da fila
status
motivo
data de criação
data de processamento

Tipos utilizados:

automation
human_review
Fluxo pelo Swagger
1. Criar um chamado

Endpoint:

POST /tickets

Exemplo:

{
  "descricao": "Atualize o chamado CH-123 para prioridade alta.",
  "categoria": "atualizacao",
  "prioridade": "alta",
  "area_solicitante": "Suporte"
}
2. Processar o chamado

Endpoint:

POST /tickets/{ticket_id}/process

Exemplo:

POST /tickets/CH-001/process

O sistema:

Analisa o chamado com o agente de IA.
Extrai os dados relevantes.
Avalia a solicitação.
Aplica as regras determinísticas.
Decide entre automação e revisão humana.
Se aprovado, executa o RPA.
Registra o resultado.
Registra a evidência da execução.
Atualiza o ticket.
Em caso de falha, cria uma entrada para tratamento humano.
Consultar chamados

Listar chamados:

GET /tickets

Consultar um chamado específico:

GET /tickets/{ticket_id}

Atualizar um chamado:

PATCH /tickets/{ticket_id}

Consultar filas:

GET /tickets/queues
Casos de validação
Inconsistência de chamados

Entrada:

Atualize o chamado CH-123 para prioridade alta,
mas os dados do cliente pertencem ao chamado CH-456.

Resultado:

revisao_humana

A automação não é executada e a justificativa registra a inconsistência.

Ação ampla

Entrada:

Fechar todos os chamados da área Financeiro.

Resultado:

revisao_humana

A solicitação não é executada automaticamente por possuir escopo amplo.

Dados essenciais ausentes

Entrada:

Atualize a prioridade do chamado.

Resultado:

revisao_humana

O sistema não inventa a prioridade ausente.

Solicitação válida

Entrada:

Atualize o chamado CH-123 para prioridade alta.

Resultado:

automacao

A atividade pode seguir para o RPA Web.

Automação Desktop

Entrada:

Calcule 10 + 5 na Calculadora.

Resultado:

automacao

O resultado real obtido pela Calculadora é registrado junto com a evidência.

Falha do RPA

Quando uma automação autorizada falha:

automation → failed
human_review → pending

O chamado é encaminhado para tratamento humano.

Testes

Teste do agente:

python test_agent.py

Teste do motor de decisão:

python test_decision.py

Teste do RPA Web:

python test_browser_rpa.py

Teste do RPA Desktop:

python test_desktop_rpa.py

Teste do agente para atividade Desktop:

python test_desktop_agent.py
Estrutura do projeto
automation-pro/

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
│   ├── models.py
│   ├── ticket_processor.py
│   └── main.py
│
├── mock_web/
│   └── index.html
│
├── evidence/
│
├── logs/
│
├── tests/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── test_agent.py
├── test_decision.py
├── test_browser_rpa.py
├── test_desktop_rpa.py
└── test_desktop_agent.py
Logs

Os logs da aplicação devem ser armazenados em:

logs/

O objetivo é permitir o acompanhamento de:

processamento dos tickets;
decisões do agente;
execução dos robôs;
resultados;
falhas;
encaminhamentos para revisão humana.
Segurança

Credenciais e configurações sensíveis não devem ser armazenadas diretamente no código-fonte.

Variáveis de ambiente devem ser utilizadas para informações sensíveis.

O arquivo .env deve permanecer fora do versionamento.

O arquivo .env.example deve conter apenas as variáveis necessárias e valores de exemplo.

Decisões técnicas
IA local

Foi utilizado Ollama com gpt-oss:20b, permitindo executar o modelo localmente sem depender de uma API externa para o processamento dos chamados.

Decisão determinística

A IA é responsável pela interpretação do chamado, mas as regras críticas de liberação da automação são aplicadas pelo código.

Isso reduz o risco de uma decisão livre do modelo executar uma operação indevida.

RPA separado por contexto

O projeto utiliza:

Playwright para automação Web;
pywinauto para automação Desktop.

Cada automação retorna resultado e evidência para que o processamento do ticket possa registrar o resultado da execução.

Revisão humana

A revisão humana funciona como mecanismo de segurança para situações de baixa confiança, dados incompletos, inconsistências, atividades de risco, ações amplas e falhas de automação.
## Front-end

Não há requisito de desenvolvimento de um front-end completo neste desafio.

A interface necessária para a demonstração é atendida por:

- Swagger/OpenAPI do FastAPI para criação, processamento e consulta dos tickets;
- aplicação Web local em `mock_web/index.html`, utilizada como alvo da automação Playwright;
- Calculadora do Windows, utilizada como alvo da automação Desktop com pywinauto.

Portanto, não é necessário React, Next.js, Vue ou outro framework de front-end para atender ao escopo do projeto.

## Testes

### Testes individuais

Teste do agente:

```powershell
python test_agent.py
```

Teste do motor de decisão:

```powershell
python test_decision.py
```

Teste do RPA Web:

```powershell
python test_browser_rpa.py
```

Teste do RPA Desktop:

```powershell
python test_desktop_rpa.py
```

### Teste dos 10 tickets

Os 10 cenários de demonstração estão documentados em:

```text
samples/tickets.json
```

Para criar e processar os 10 automaticamente pela API:

```powershell
python scripts/test_10_tickets.py
```

A API deve estar em execução antes:

```powershell
uvicorn app.main:app --reload
```

O conjunto inclui:

1. RPA Web com sucesso
2. RPA Desktop com sucesso
3. Inconsistência entre chamados
4. Solicitação em massa
5. Dados essenciais ausentes
6. Baixa confiança
7. Segundo cenário Web
8. Segundo cenário Desktop
9. Falha controlada do RPA Web
10. Consulta/atividade fora do escopo de automação

O cenário de falha do RPA é demonstrado temporariamente alterando o seletor do botão no `app/rpa/browser.py`. Após a demonstração, o seletor original deve ser restaurado.

## Estrutura do projeto

```text
automation-pro/
│
├── app/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── prompts.py
│   │   └── schemas.py
│   ├── rpa/
│   │   ├── browser.py
│   │   └── desktop.py
│   ├── routes/
│   │   └── tickets.py
│   ├── services/
│   │   └── decision.py
│   ├── database.py
│   ├── database_models.py
│   ├── logging_config.py
│   ├── models.py
│   ├── ticket_processor.py
│   └── main.py
├── mock_web/
│   └── index.html
├── samples/
│   └── tickets.json
├── scripts/
│   └── test_10_tickets.py
├── evidence/
├── logs/
├── tests/
├── .env.example
├── .gitignore
├── ARCHITECTURE.md
├── README.md
└── requirements.txt
```



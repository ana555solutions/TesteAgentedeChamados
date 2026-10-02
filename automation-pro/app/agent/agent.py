import json
import ollama

from app.agent.prompts import SYSTEM_PROMPT, build_user_prompt
from app.agent.schemas import AgentResult


class TicketAgent:
    def __init__(self):
        self.model = "gpt-oss:20b"

    def analyze(self, ticket: dict) -> AgentResult:
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                    + """

IMPORTANTE:
Retorne SOMENTE um objeto JSON válido.
Não use Markdown.
Não use ```json.
Não escreva explicações antes ou depois do JSON.

Use exatamente estes nomes de campos:
classificacao
resumo
dados_extraidos
atividade_solicitada
decisao
confianca
justificativa
campos_faltantes
risco

Dentro de dados_extraidos, use exatamente:
numero_chamado_alvo
numero_chamado_dados
prioridade_solicitada
area_solicitante
resultado_solicitado
numero_1
numero_2
outros_dados
""",
                },
                {
                    "role": "user",
                    "content": build_user_prompt(ticket),
                },
            ],
            format="json",
        )

        content = response["message"]["content"].strip()

        data = json.loads(content)

        if "classification" in data:
            data["classificacao"] = data.pop("classification")

        if "atividade" in data:
            data["atividade_solicitada"] = data.pop("atividade")

        if "confiança" in data:
            data["confianca"] = data.pop("confiança")

        dados = data.get("dados_extraidos", {})

        if "resultado_solicitado" in dados and dados["resultado_solicitado"] is not None:
            dados["resultado_solicitado"] = str(dados["resultado_solicitado"])

        if not isinstance(dados.get("outros_dados"), dict):
            dados["outros_dados"] = {}

        data["dados_extraidos"] = dados
        
        return AgentResult.model_validate(data)
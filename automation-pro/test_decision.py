from app.agent.schemas import AgentResult, ExtractedData
from app.services.decision import evaluate_decision


result = AgentResult(
    classificacao="atualizacao",
    resumo="Atualizar prioridade do chamado CH-123 para alta.",
    dados_extraidos=ExtractedData(
        numero_chamado_alvo="CH-123",
        numero_chamado_dados=None,
        prioridade_solicitada="alta",
        area_solicitante="Suporte",
        resultado_solicitado=None,
        outros_dados={},
    ),
    atividade_solicitada="Atualizar prioridade de chamado existente",
    decisao="automacao",
    confianca=90,
    justificativa="Dados completos.",
    campos_faltantes=[],
    risco="baixo",
)


decisao, justificativa = evaluate_decision(result)

print("DECISÃO:", decisao)
print("JUSTIFICATIVA:", justificativa)
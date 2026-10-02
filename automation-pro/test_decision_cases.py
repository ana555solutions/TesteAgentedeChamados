from app.agent.schemas import AgentResult, ExtractedData
from app.services.decision import evaluate_decision


result = AgentResult(
    classificacao="atualizacao",
    resumo="Atualizar a prioridade do chamado CH-123 para alta.",
    dados_extraidos=ExtractedData(
        numero_chamado_alvo="CH-123",
        numero_chamado_dados=None,
        prioridade_solicitada="alta",
        area_solicitante="Suporte",
    ),
    atividade_solicitada="Alterar prioridade do chamado",
    decisao="automacao",
    confianca=95,
    justificativa="Dados completos e consistentes.",
    campos_faltantes=[],
    risco="baixo",
)


decision, reason = evaluate_decision(result)

print("DECISÃO:", decision)
print("MOTIVO:", reason)
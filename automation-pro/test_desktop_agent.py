from app.agent.agent import TicketAgent


agent = TicketAgent()

ticket = {
    "id": "CH-004",
    "descricao": "Calcule 10 + 5 na Calculadora.",
    "categoria": None,
    "prioridade": None,
    "area_solicitante": "Suporte",
}

result = agent.analyze(ticket)

print("CLASSIFICAÇÃO:", result.classificacao)
print("ATIVIDADE:", result.atividade_solicitada)
print("DECISÃO:", result.decisao)
print("CONFIANÇA:", result.confianca)
print("NÚMERO 1:", result.dados_extraidos.numero_1)
print("NÚMERO 2:", result.dados_extraidos.numero_2)
print("JUSTIFICATIVA:", result.justificativa)
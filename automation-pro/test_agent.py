from app.agent.agent import TicketAgent


ticket = {
    "id": "CH-003",
    "descricao": "Atualize a prioridade do chamado.",
    "categoria": "atualizacao",
    "prioridade": None,
    "area_solicitante": "Suporte",
}


agent = TicketAgent()
result = agent.analyze(ticket)

print(result.model_dump_json(indent=2))
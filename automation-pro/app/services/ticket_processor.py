from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.agent.agent import TicketAgent
from app.services.decision import evaluate_decision
from app.database_models import TicketDB, QueueItemDB
from app.rpa.browser import update_ticket_priority
from app.rpa.desktop import execute_desktop_calculation
from app.logging_config import logger


def process_ticket(ticket: TicketDB, db: Session):
    logger.info(f"Processando ticket {ticket.id}")

    agent = TicketAgent()

    agent_result = agent.analyze({
        "id": ticket.id,
        "descricao": ticket.descricao,
        "categoria": ticket.categoria,
        "prioridade": ticket.prioridade,
        "area_solicitante": ticket.area_solicitante,
    })

    decision, reason = evaluate_decision(agent_result, ticket.id)

    logger.info(
        f"Ticket {ticket.id} | decisão={decision} | "
        f"confiança={agent_result.confianca:.0f}%"
    )

    ticket.resumo = agent_result.resumo
    ticket.dados_extraidos = agent_result.dados_extraidos.model_dump()
    ticket.decisao = decision
    ticket.confianca = agent_result.confianca
    ticket.justificativa = reason

    if decision == "revisao_humana":
        logger.info(
            f"Ticket {ticket.id} encaminhado para revisão humana | "
            f"motivo={reason}"
        )

        ticket.status = "revisao_humana"

        queue_item = QueueItemDB(
            ticket_id=ticket.id,
            queue_type="human_review",
            status="pending",
            reason=reason,
            created_at=datetime.now(timezone.utc),
        )

        db.add(queue_item)
        db.commit()
        db.refresh(ticket)

        return ticket, agent_result, queue_item

    queue_item = QueueItemDB(
        ticket_id=ticket.id,
        queue_type="automation",
        status="processing",
        reason=reason,
        created_at=datetime.now(timezone.utc),
    )

    db.add(queue_item)
    db.commit()

    logger.info(
        f"Ticket {ticket.id} | iniciando automação RPA"
    )

    try:
        dados = agent_result.dados_extraidos
        atividade = agent_result.atividade_solicitada.lower()

        # Automação Desktop
        if any(
            termo in atividade
            for termo in ["calcular", "calculadora", "cálculo"]
        ):
            logger.info(
                f"Ticket {ticket.id} | executando RPA Desktop"
            )

            if dados.numero_1 is None or dados.numero_2 is None:
                raise ValueError(
                    "Os dois números necessários para o cálculo não foram informados."
                )

            rpa_result = execute_desktop_calculation(
                number_1=dados.numero_1,
                number_2=dados.numero_2,
            )

        # Automação Web
        else:
            logger.info(
                f"Ticket {ticket.id} | executando RPA Web"
            )

            ticket_id_alvo = dados.numero_chamado_alvo
            prioridade = dados.prioridade_solicitada

            if not ticket_id_alvo or prioridade is None:
                raise ValueError(
                    "Dados insuficientes para executar a automação."
                )

            rpa_result = update_ticket_priority(
                ticket_id=ticket_id_alvo,
                priority=prioridade,
            )

        ticket.status = "concluido"
        ticket.resultado = rpa_result["resultado"]
        ticket.evidencias = [rpa_result["evidencia"]]

        queue_item.status = "completed"
        queue_item.processed_at = datetime.now(timezone.utc)

        logger.info(
            f"Ticket {ticket.id} | automação concluída com sucesso"
        )

    except Exception as exc:
        logger.error(
            f"Ticket {ticket.id} | falha na automação: {exc}",
            exc_info=True,
        )

        ticket.status = "falhou"
        ticket.resultado = f"Falha na automação: {exc}"

        queue_item.status = "failed"
        queue_item.processed_at = datetime.now(timezone.utc)

        human_queue_item = QueueItemDB(
            ticket_id=ticket.id,
            queue_type="human_review",
            status="pending",
            reason="A automação falhou e o chamado precisa de tratamento humano.",
            created_at=datetime.now(timezone.utc),
        )

        db.add(human_queue_item)

        logger.info(
            f"Ticket {ticket.id} | encaminhado para revisão humana após falha"
        )

    db.commit()
    db.refresh(ticket)

    return ticket, agent_result, queue_item
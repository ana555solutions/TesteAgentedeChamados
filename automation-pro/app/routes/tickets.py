from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.database_models import TicketDB, QueueItemDB
from app.models import Ticket, TicketCreate, TicketUpdate
from app.services.ticket_processor import process_ticket


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post("", response_model=Ticket, status_code=201)
def create_ticket(
    data: TicketCreate,
    db: Session = Depends(get_db),
):
    last_ticket = (
        db.query(TicketDB)
        .order_by(TicketDB.id.desc())
        .first()
    )

    if last_ticket:
        last_number = int(last_ticket.id.split("-")[1])
        next_number = last_number + 1
    else:
        next_number = 1

    ticket_id = f"CH-{next_number:03d}"

    now = datetime.now(timezone.utc)

    ticket = TicketDB(
        id=ticket_id,
        descricao=data.descricao,
        categoria=data.categoria,
        prioridade=data.prioridade,
        area_solicitante=data.area_solicitante,
        criado_em=now,
        atualizado_em=now,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


@router.get("", response_model=list[Ticket])
def list_tickets(
    db: Session = Depends(get_db),
):
    return db.query(TicketDB).all()


@router.get("/queues")
def get_queues(
    db: Session = Depends(get_db),
):
    items = (
        db.query(QueueItemDB)
        .order_by(QueueItemDB.created_at.desc())
        .all()
    )

    return [
        {
            "id": item.id,
            "ticket_id": item.ticket_id,
            "queue_type": item.queue_type,
            "status": item.status,
            "reason": item.reason,
            "created_at": item.created_at,
            "processed_at": item.processed_at,
        }
        for item in items
    ]


@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
):
    ticket = db.get(TicketDB, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Chamado não encontrado",
        )

    return ticket


@router.patch("/{ticket_id}", response_model=Ticket)
def update_ticket(
    ticket_id: str,
    data: TicketUpdate,
    db: Session = Depends(get_db),
):
    ticket = db.get(TicketDB, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Chamado não encontrado",
        )

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(ticket, field, value)

    ticket.atualizado_em = datetime.now(timezone.utc)

    db.commit()
    db.refresh(ticket)

    return ticket


@router.post("/{ticket_id}/process", response_model=Ticket)
def process_ticket_endpoint(
    ticket_id: str,
    db: Session = Depends(get_db),
):
    ticket = db.get(TicketDB, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Chamado não encontrado",
        )

    ticket, _, _ = process_ticket(ticket, db)

    return ticket
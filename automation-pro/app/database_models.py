from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TicketDB(Base):
    __tablename__ = "tickets"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)

    descricao: Mapped[str] = mapped_column(Text)
    categoria: Mapped[str | None] = mapped_column(String(100), nullable=True)
    prioridade: Mapped[str | None] = mapped_column(String(50), nullable=True)
    area_solicitante: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    resumo: Mapped[str | None] = mapped_column(Text, nullable=True)

    dados_extraidos: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
    )

    decisao: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    confianca: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    justificativa: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="aberto",
    )

    resultado: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    evidencias: Mapped[list] = mapped_column(
        JSON,
        default=list,
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

class QueueItemDB(Base):
    __tablename__ = "queue_items"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    ticket_id: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    queue_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
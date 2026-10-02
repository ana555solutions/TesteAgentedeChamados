from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    descricao: str
    categoria: str | None = None
    prioridade: str | None = None
    area_solicitante: str | None = None


class TicketUpdate(BaseModel):
    categoria: str | None = None
    prioridade: str | None = None
    area_solicitante: str | None = None
    resumo: str | None = None
    dados_extraidos: dict[str, Any] | None = None
    decisao: str | None = None
    confianca: float | None = Field(default=None, ge=0, le=1)
    justificativa: str | None = None
    status: str | None = None
    resultado: str | None = None
    evidencias: list[str] | None = None


class Ticket(TicketCreate):
    id: str
    resumo: str | None = None
    dados_extraidos: dict[str, Any] = {}
    decisao: str | None = None
    confianca: float | None = None
    justificativa: str | None = None
    status: str = "aberto"
    resultado: str | None = None
    evidencias: list[str] = []
    criado_em: datetime
    atualizado_em: datetime
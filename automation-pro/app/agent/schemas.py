from typing import Any

from pydantic import BaseModel, Field


class ExtractedData(BaseModel):
    numero_chamado_alvo: str | None = Field(
        default=None,
        description="Número do chamado que será alterado, consultado ou utilizado na atividade.",
    )

    numero_chamado_dados: str | None = Field(
        default=None,
        description="Número do chamado ao qual pertencem os dados utilizados na execução, quando informado.",
    )

    prioridade_solicitada: str | None = Field(
        default=None,
        description="Nova prioridade solicitada, quando aplicável.",
    )

    area_solicitante: str | None = Field(
        default=None,
        description="Área que solicitou a atividade.",
    )

    resultado_solicitado: str | None = Field(
        default=None,
        description="Resultado, cálculo ou informação solicitada, quando aplicável.",
    )

    numero_1: int | None = Field(
        default=None,
        description="Primeiro número de uma operação matemática, quando aplicável.",
    )

    numero_2: int | None = Field(
        default=None,
        description="Segundo número de uma operação matemática, quando aplicável.",
    )

    outros_dados: dict[str, Any] = Field(
        default_factory=dict,
        description="Outros dados explicitamente presentes no chamado e necessários para a atividade.",
    )


class AgentResult(BaseModel):
    classificacao: str
    resumo: str
    dados_extraidos: ExtractedData
    atividade_solicitada: str
    decisao: str
    confianca: float = Field(ge=0, le=100)
    justificativa: str
    campos_faltantes: list[str] = Field(default_factory=list)
    risco: str
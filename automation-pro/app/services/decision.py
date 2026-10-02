from app.agent.schemas import AgentResult


CONFIDENCE_THRESHOLD = 80


def evaluate_decision(
    result: AgentResult,
    ticket_id: str | None = None,
) -> tuple[str, str]:

    # 1. Confiança abaixo do limite
    if result.confianca < CONFIDENCE_THRESHOLD:
        return (
            "revisao_humana",
            (
                f"Confiança da análise ({result.confianca:.0f}%) "
                f"abaixo do limite definido de "
                f"{CONFIDENCE_THRESHOLD}%."
            ),
        )

    dados = result.dados_extraidos

    # 2. Inconsistência entre chamado alvo e chamado dos dados
    chamado_alvo = dados.numero_chamado_alvo
    chamado_dados = dados.numero_chamado_dados

    if (
        chamado_alvo
        and chamado_dados
        and chamado_alvo != chamado_dados
    ):
        return (
            "revisao_humana",
            (
                "Inconsistência identificada: o chamado alvo é "
                f"{chamado_alvo}, mas os dados apresentados pertencem "
                f"ao chamado {chamado_dados}."
            ),
        )

    # 3. Risco alto
    if result.risco.lower() == "alto":
        return (
            "revisao_humana",
            "A atividade foi classificada como de alto risco.",
        )

    # 4. Solicitações amplas
    atividade = result.atividade_solicitada.lower()

    termos_amplos = [
        "todos",
        "todas",
        "em massa",
        "massivamente",
    ]

    if any(termo in atividade for termo in termos_amplos):
        return (
            "revisao_humana",
            (
                "A solicitação possui escopo amplo e requer "
                "validação humana antes da execução."
            ),
        )

    # 5. Campos realmente essenciais para a atividade
    if result.classificacao == "atualizacao":
        if not dados.numero_chamado_alvo:
            return (
                "revisao_humana",
                "Número do chamado alvo não informado.",
            )

        if dados.prioridade_solicitada is None:
            return (
                "revisao_humana",
                "Nova prioridade não informada para a atualização.",
            )

    # 6. Decisão final
    return (
        "automacao",
        (
            f"Dados necessários identificados, risco aceitável e "
            f"confiança de {result.confianca:.0f}% acima do limite de "
            f"{CONFIDENCE_THRESHOLD}%. Solicitação elegível para automação."
        ),
    )

import json
import sys
import time
from pathlib import Path

import requests

BASE_URL = "http://127.0.0.1:8000"
SAMPLES_FILE = Path(__file__).resolve().parents[1] / "samples" / "tickets.json"


def main():
    tickets = json.loads(SAMPLES_FILE.read_text(encoding="utf-8"))

    print("=" * 80)
    print("TESTE DOS 10 TICKETS - AUTOMATION PRO")
    print("=" * 80)

    try:
        requests.get(f"{BASE_URL}/health", timeout=5).raise_for_status()
    except Exception as exc:
        print(f"\nAPI indisponível: {exc}")
        print("Execute primeiro: uvicorn app.main:app --reload")
        sys.exit(1)

    resultados = []

    for index, sample in enumerate(tickets, start=1):
        payload = {
            "descricao": sample["descricao"],
            "categoria": sample.get("categoria"),
            "prioridade": sample.get("prioridade"),
            "area_solicitante": sample.get("area_solicitante"),
        }

        print(f"\n[{index:02d}/10] {sample['nome']}")
        print(f"Descrição: {sample['descricao']}")
        print(f"Esperado:  {sample['esperado']}")

        try:
            response = requests.post(
                f"{BASE_URL}/tickets",
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            ticket = response.json()
            ticket_id = ticket["id"]

            print(f"Criado:    {ticket_id}")

            response = requests.post(
                f"{BASE_URL}/tickets/{ticket_id}/process",
                timeout=180,
            )
            response.raise_for_status()
            result = response.json()

            print(f"Decisão:   {result.get('decisao')}")
            print(f"Confiança: {result.get('confianca')}%")
            print(f"Status:    {result.get('status')}")
            print(f"Resultado: {result.get('resultado')}")

            resultados.append({
                "nome": sample["nome"],
                "ticket_id": ticket_id,
                "decisao": result.get("decisao"),
                "confianca": result.get("confianca"),
                "status": result.get("status"),
                "resultado": result.get("resultado"),
            })

        except Exception as exc:
            print(f"ERRO: {exc}")
            resultados.append({
                "nome": sample["nome"],
                "erro": str(exc),
            })

    print("\n" + "=" * 80)
    print("RESUMO")
    print("=" * 80)

    for result in resultados:
        if "erro" in result:
            print(f"{result['nome']}: ERRO")
        else:
            print(
                f"{result['ticket_id']} | "
                f"{result['nome']} | "
                f"{result['decisao']} | "
                f"{result['status']}"
            )


if __name__ == "__main__":
    main()

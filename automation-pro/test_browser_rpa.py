from app.rpa.browser import update_ticket_priority


result = update_ticket_priority(
    ticket_id="CH-123",
    priority="alta",
)

print("RESULTADO:")
print(result["resultado"])

print("EVIDÊNCIA:")
print(result["evidencia"])
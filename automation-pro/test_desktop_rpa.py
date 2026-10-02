from app.rpa.desktop import execute_desktop_calculation


result = execute_desktop_calculation(
    number_1=10,
    number_2=5,
)

print("RESULTADO:")
print(result["resultado"])

print("EVIDÊNCIA:")
print(result["evidencia"])
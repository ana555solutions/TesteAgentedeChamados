from pathlib import Path
import time

from PIL import ImageGrab
from pywinauto import Application
from pywinauto.keyboard import send_keys


EVIDENCE_DIR = Path(__file__).resolve().parents[2] / "evidence"


def execute_desktop_calculation(
    number_1: int,
    number_2: int,
) -> dict:

    EVIDENCE_DIR.mkdir(exist_ok=True)

    screenshot_path = EVIDENCE_DIR / "desktop_calculator.png"

    Application(backend="uia").start("calc.exe")

    app = Application(backend="uia").connect(
        title_re=".*Calculadora.*",
        timeout=10,
    )

    window = app.window(title_re=".*Calculadora.*")
    window.set_focus()

    time.sleep(1)

    # Digita o primeiro número
    send_keys(str(number_1))

    # Clica no botão "+"
    window.child_window(
        auto_id="plusButton",
        control_type="Button",
    ).click_input()

    # Digita o segundo número
    send_keys(str(number_2))

    # Clica no botão "="
    window.child_window(
        auto_id="equalButton",
        control_type="Button",
    ).click_input()

    time.sleep(1)

    # Lê o resultado REAL exibido pela Calculadora
    result_control = window.child_window(
        auto_id="CalculatorResults",
        control_type="Text",
    )

    result_text = result_control.window_text()

    # Captura evidência depois do cálculo
    rect = window.rectangle()

    screenshot = ImageGrab.grab(
        bbox=(
            rect.left,
            rect.top,
            rect.right,
            rect.bottom,
        )
    )

    screenshot.save(screenshot_path)

    app.kill()

    return {
        "resultado": result_text,
        "evidencia": str(screenshot_path),
    }
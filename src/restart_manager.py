from pathlib import Path
import subprocess
import sys
import os
import time

from bot_controller import (
    get_driver,
    cerrar_driver
)

BASE_DIR = Path(__file__).resolve().parent
MAIN_PATH = BASE_DIR / "main.py"


def reinicio_completo():

    print("🔄 Ejecutando reinicio completo...")
    import os

    print(
        f"PID REINICIANDO: {os.getpid()}"
    )
    try:

        driver = get_driver()

        cerrar_driver(driver)

    except Exception as e:

        print(f"⚠ Error cerrando driver: {e}")

    time.sleep(2)

    print(f"Python: {sys.executable}")
    print(f"Main: {MAIN_PATH}")
    print(
        f"PID ACTUAL: {os.getpid()}"
    )
    

    subprocess.Popen(
        [
            sys.executable,
            str(MAIN_PATH)
        ],
        cwd=str(BASE_DIR)
    )
    print(
        "CERRANDO PROCESO ACTUAL"
    )
    os._exit(0)
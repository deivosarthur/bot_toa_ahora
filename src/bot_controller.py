from login import iniciar_sesion
import time


driver_global = None


def set_driver(driver):

    global driver_global

    driver_global = driver


def get_driver():

    return driver_global


def cerrar_driver(driver):

    try:

        if driver:

            driver.quit()

            print(
                "🛑 Driver cerrado correctamente"
            )

    except Exception as e:

        print(
            f"⚠ Error cerrando driver: {e}"
        )


def reiniciar_bot():

    global driver_global

    print("🔄 Reiniciando bot...")

    # 🔥 cerrar SOLO este driver
    cerrar_driver(driver_global)

    # 🔥 esperar liberación real
    time.sleep(5)

    # 🔥 iniciar nuevo driver
    driver_global = iniciar_sesion()

    print("✅ Bot reiniciado correctamente")

    return driver_global
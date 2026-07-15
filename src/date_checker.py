from datetime import datetime
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Meses en español
MESES = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}


def obtener_fecha_toa(driver):
    """
    Obtiene el texto de la fecha mostrada en TOA.

    Ejemplo:
        Miércoles 15 Julio 2026
    """

    boton_fecha = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, "toolbar-date-button-value")
        )
    )

    fecha = boton_fecha.get_attribute("title").strip()

    return fecha


def convertir_fecha_toa(fecha_texto):
    """
    Convierte:

        'Miércoles 15 Julio 2026'

    a

        datetime.date(2026, 7, 15)
    """

    partes = fecha_texto.split()

    # partes = ['Miércoles', '15', 'Julio', '2026']

    dia = int(partes[1])

    mes = MESES[partes[2].lower()]

    año = int(partes[3])

    return datetime(año, mes, dia).date()


def fecha_toa_es_hoy(driver, logger=None):

    fecha_texto = obtener_fecha_toa(driver)

    fecha_toa = convertir_fecha_toa(fecha_texto)

    fecha_pc = datetime.now().date()

    mensaje = (
        f"Fecha TOA: {fecha_toa}\n"
        f"Fecha PC : {fecha_pc}"
    )

    if logger:
        logger.info(mensaje)
    else:
        print(mensaje)

    if fecha_toa == fecha_pc:

        if logger:
            logger.info("Fecha correcta")
        else:
            print("Fecha correcta")

        return True

    else:

        if logger:
            logger.warning("La fecha de TOA está desactualizada")
        else:
            print("La fecha de TOA está desactualizada")

        return False
    
def click_siguiente(driver):
    boton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.ID,
                "dc__top_panel__date_picker__popup--button-next"
            )
        )
    )

    boton.click()
    
def click_anterior(driver):
    boton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.ID,
                "dc__top_panel__date_picker__popup--button-previous"
            )
        )
    )

    boton.click()
    
def sincronizar_fecha_toa(driver, logger=None):
    """
    Verifica que la fecha seleccionada en TOA corresponda al día actual.
    Si está desfasada, avanza o retrocede automáticamente hasta sincronizarla.
    """

    from datetime import datetime
    import time

    fecha_pc = datetime.now().date()

    fecha_toa = convertir_fecha_toa(
        obtener_fecha_toa(driver)
    )

    if logger:
        logger.info(f"📅 Fecha TOA : {fecha_toa}")
        logger.info(f"📅 Fecha PC  : {fecha_pc}")

    # Ya está correcta
    if fecha_toa == fecha_pc:

        if logger:
            logger.info("✅ La fecha de TOA ya está sincronizada.")
        else:
            print("✅ La fecha de TOA ya está sincronizada.")

        return True

    if logger:
        logger.warning(
            f"⚠️ Fecha desactualizada ({fecha_toa}). Iniciando sincronización..."
        )
    else:
        print(
            f"⚠️ Fecha desactualizada ({fecha_toa}). Iniciando sincronización..."
        )

    intentos = 0
    MAX_INTENTOS = 10

    while fecha_toa != fecha_pc:

        intentos += 1

        if intentos > MAX_INTENTOS:
            raise Exception(
                "No fue posible sincronizar la fecha de TOA."
            )

        # Guardamos la fecha actual que muestra TOA
        fecha_anterior = obtener_fecha_toa(driver)

        if fecha_toa < fecha_pc:

            if logger:
                logger.info("➡️ Avanzando un día...")

            click_siguiente(driver)

        else:

            if logger:
                logger.info("⬅️ Retrocediendo un día...")

            click_anterior(driver)

        # Espera hasta que el texto cambie
        esperar_cambio_fecha(driver, fecha_anterior)

        fecha_toa = convertir_fecha_toa(
            obtener_fecha_toa(driver)
        )

        if logger:
            logger.info(f"📅 Nueva fecha TOA: {fecha_toa}")

        return True

def esperar_cambio_fecha(driver, fecha_anterior):
    """
    Espera hasta que TOA actualice el texto de la fecha.
    """

    WebDriverWait(driver, 10).until(
        lambda d: obtener_fecha_toa(d) != fecha_anterior
    )
    
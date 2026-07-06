from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from file_manager import esperar_descarga, renombrar_y_mover
from file_manager import archivo_reciente
from bot_state import BOT_STATE
from heartbeat import guardar_estado
from db import insertar_descarga

import logging
import time

log = logging.getLogger()

def descargar_area(driver, area_id, nombre):
    
    wait = WebDriverWait(driver, 25)
    
    BOT_STATE["mensaje"] = (
        f"Descargando {nombre}"
    )

    guardar_estado()

    log.info(f"Procesando área {area_id}")
    
    
    if archivo_reciente(nombre):
        log.info(f"⏭️ {nombre} ya descargado recientemente, se omite")
        return

    # 1️⃣ Seleccionar área
    area_label = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//div[@data-id='{area_id}']//button[contains(@class,'edt-label')]")
    ))
    driver.execute_script("arguments[0].click();", area_label)

    log.info("✔ Área seleccionada")

    time.sleep(2)
    

    # 2️⃣ Click en botón "Acciones" (barra superior)
    acciones_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@title='Acciones']")
    ))
    driver.execute_script("arguments[0].click();", acciones_btn)

    log.info("✔ Menú Acciones abierto")

    # 3️⃣ Esperar menú desplegado
    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, "app-menu-container")
    ))
    
    

    # 4️⃣ Click en "Imprimir ruta"
    imprimir_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[text()='Exportar']/ancestor::button")
    ))
    driver.execute_script("arguments[0].click();", imprimir_btn)

    log.info("✔ Exportar ejecutado")

    # 5️⃣ Esperar descarga
    archivo = esperar_descarga()

    if archivo:
        renombrar_y_mover(archivo)
        insertar_descarga(nombre, archivo)
        return True
    else:
        return False


# devolver áreas procesadas
def ejecutar_descargas(driver):
    
   
    AREAS = {
        "metropolitana": "5",
        "norte": "6",
        "sur": "8",
        "centro": "4"
    }

    procesadas = []

    for nombre, area_id in AREAS.items():
        ok = descargar_area(driver, area_id, nombre)
        if ok:
            procesadas.append(nombre)

    return procesadas
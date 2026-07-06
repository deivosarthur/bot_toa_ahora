from datetime import datetime

from db import init_db

from db import registrar_evento
from login import iniciar_sesion
from downloader import ejecutar_descargas
from utils import setup_logger
from file_manager import crear_flag, limpiar_screenshots, notificar

#from file_manager import actualizar_estado
import time
from bot_controller import set_driver
import threading
from bot_controller import reiniciar_bot

from dashboard import app
from file_manager import limpiar_temporales
from file_manager import guardar_screenshot
from file_manager import entregar_archivos_finales
from file_manager import actualizar_runtime
from waitress import serve
from command_listener import (
    procesar_comandos
)

from bot_state import BOT_STATE
from heartbeat import guardar_estado

def iniciar_dashboard():
    serve(
        app,
        host="0.0.0.0",
        port=5000
    )
    
def main():
    
    import os

    print(
        f"PID BOT: {os.getpid()}"
    )
    
    init_db()  # 🔥 ESTO PRIMERO
     
    # iniciar dashboard en paralelo
    threading.Thread(target=iniciar_dashboard, daemon=True).start()

    logger = setup_logger()
    driver = iniciar_sesion()
    set_driver(driver)
    #actualizar_estado("ACTIVO")
    limpiar_screenshots()
    logger.info("Bot iniciado correctamente")
    
    BOT_STATE["pid_bot"] = os.getpid()
    BOT_STATE["pid_chromedriver"] = (driver.service.process.pid)
    BOT_STATE["pid_chrome"] = (driver.capabilities["goog:processID"])
    BOT_STATE["estado"] = "INICIANDO"

    BOT_STATE["mensaje"] = (
        "Bot iniciado"
    )


    guardar_estado()

    while True:
        

        BOT_STATE["ultima_actualizacion"] = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        guardar_estado()
        try:
            comando = procesar_comandos()

            if comando:

                logger.info(
                    "📨 Reinicio remoto solicitado"
                )

                registrar_evento(
                    "REMOTE_RESTART",
                    "Reinicio solicitado desde Dashboard"
                )

                BOT_STATE["reinicios"] += 1

                BOT_STATE["mensaje"] = (
                    "Reinicio remoto"
                )

                guardar_estado()

                driver = reiniciar_bot()

                if driver:

                        set_driver(driver)

                        BOT_STATE["pid_chromedriver"] = (
                            driver.service.process.pid
                        )

                        BOT_STATE["pid_chrome"] = (
                            driver.capabilities["goog:processID"]
                        )

                        guardar_estado()

                continue
            
            
            BOT_STATE["estado"] = "DESCARGANDO"

            BOT_STATE["mensaje"] = (
                "Procesando áreas"
            )

            guardar_estado()
            
            logger.info("🔄 Iniciando ciclo de descarga")

            registrar_evento(
                "CICLO_INICIO",
                "Inicio de ciclo de descarga"
            )

            # 🔥 limpieza
            limpiar_temporales()

            # 🔥 descargas
            areas_ok = ejecutar_descargas(driver)

            # 🔥 SOLO si hubo cambios
            if areas_ok:

                entregar_archivos_finales()

                crear_flag(areas_ok)

                #actualizar_estado("ACTIVO")

                notificar(
                    f"✅ Descargas OK: {areas_ok}"
                )

                logger.info(
                    f"✅ Áreas procesadas: {areas_ok}"
                )
                BOT_STATE["estado"] = "OK"

                BOT_STATE["mensaje"] = (
                    f"Áreas procesadas: {areas_ok}"
                )

                BOT_STATE["ciclos_ok"] += 1

                BOT_STATE["ultima_descarga"] = (
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )

                guardar_estado()
                
                registrar_evento(
                    "DESCARGA_OK",
                    str(areas_ok)
                )

            else:

                logger.info(
                    "⏭️ Sin cambios, no se genera flag"
                )

            logger.info("⏳ Esperando 5 minutos...")
            actualizar_runtime(300)
            for _ in range(300):

                if _ % 30 == 0:

                    BOT_STATE["ultima_actualizacion"] = (
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    )

                    guardar_estado()

                time.sleep(1)
                
        except Exception as e:
            
            registrar_evento(
                "ERROR",
                str(e)
            )
            BOT_STATE["estado"] = "ERROR"

            BOT_STATE["mensaje"] = str(e)

            BOT_STATE["errores"] += 1

            BOT_STATE["errores_consecutivos"] += 1

            guardar_estado()

            logger.error(f"❌ Error en ciclo: {e}")

            try:

                screenshot = guardar_screenshot(driver)

            except:

                screenshot = None

            if screenshot:

                logger.error(
                    f"📸 Screenshot: {screenshot}"
                )

            notificar(f"❌ Error bot: {e}")

            #actualizar_estado("ERROR")

            print("🔄 Ejecutando reinicio completo...")

            try:

                driver = reiniciar_bot()
                
                registrar_evento(
                    "RESTART",
                    "Bot reiniciado"
                )
                
                BOT_STATE["reinicios"] += 1

                BOT_STATE["estado"] = "OK"

                BOT_STATE["mensaje"] = (
                    "Bot reiniciado correctamente"
                )

                guardar_estado()
                
                if driver:
                        set_driver(driver)

                        BOT_STATE["pid_chromedriver"] = (
                            driver.service.process.pid
                        )

                        BOT_STATE["pid_chrome"] = (
                            driver.capabilities["goog:processID"]
                        )

                        guardar_estado()
                    
                BOT_STATE["errores_consecutivos"] = 0

                BOT_STATE["alerta_error_enviada"] = False

            except Exception as reinicio_error:

                logger.error(
                    f"❌ Error reiniciando bot: {reinicio_error}"
                )
                
                
                registrar_evento(
                    "ERROR_RESTART",
                    "Error al reiniciar bot"
                )
                BOT_STATE["estado"] = "ERROR REINICIO"

                BOT_STATE["mensaje"] = str(e)

                BOT_STATE["errores"] += 1

                BOT_STATE["errores_consecutivos"] += 1

                guardar_estado()
                
                

            time.sleep(60)

if __name__ == "__main__":
    main()
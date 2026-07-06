import os
import time
import shutil
from datetime import datetime
from venv import logger
import requests
import json


from config import (
    DOWNLOAD_PATH, 
    DESTINO,
    DESTINO_HISTORICO, 
    FLAG_PATH,
    PROCESSED_PATH,
    STATE_PATH,
    META_PATH)



BOT_START = datetime.now()

def esperar_descarga():

    print("⏳ Esperando archivo...")

    tiempo_max = 60

    inicio = time.time()

    while time.time() - inicio < tiempo_max:

        archivos = [

            f for f in os.listdir(DOWNLOAD_PATH)

            if (
                f.endswith(".xlsx")
                and
                not f.endswith(".crdownload")
            )
        ]

        if archivos:

            archivo = max(
                [
                    os.path.join(DOWNLOAD_PATH, f)
                    for f in archivos
                ],
                key=os.path.getctime
            )

            # 🔥 validar tamaño estable
            size1 = os.path.getsize(archivo)

            time.sleep(2)

            size2 = os.path.getsize(archivo)

            if size1 == size2:

                print(
                    f"✔ Archivo detectado: {archivo}"
                )

                return archivo

        time.sleep(1)

    print("❌ No se detectó descarga")

    return None


def renombrar_y_mover(filepath):

    os.makedirs(DESTINO, exist_ok=True)
    os.makedirs(DESTINO_HISTORICO, exist_ok=True)

    filename = os.path.basename(filepath)

    # 🔥 nombre base
    base = filename.split("_")[0]

    # 🔥 eliminar antiguos mismo tipo
    for f in os.listdir(DESTINO):

        if f.startswith(base) and f.endswith(".xlsx"):

            try:
                os.remove(os.path.join(DESTINO, f))
            except:
                pass

    # 🔥 copia histórica
    historico_destino = os.path.join(
        DESTINO_HISTORICO,
        filename
    )

    shutil.copy2(filepath, historico_destino)

    # 🔥 mover archivo actual
    os.makedirs(PROCESSED_PATH, exist_ok=True)

    destino_final = os.path.join(
        PROCESSED_PATH,
        filename
    )

    shutil.move(filepath, destino_final)

    logger.info(f"✅ Archivo movido: {destino_final}")

    return destino_final
    
def archivo_reciente(base, minutos=3):

    ahora = time.time()

    for archivo in os.listdir(DESTINO):

        if archivo.startswith(base):

            ruta = os.path.join(DESTINO, archivo)

            tiempo_archivo = os.path.getmtime(ruta)

            if (ahora - tiempo_archivo) < minutos * 60:
                return True

    return False


#FLAGS CREACION --------------------------------------
def crear_flag(areas_procesadas):
    # escribe info útil para KNIME
    contenido = {
        "timestamp": datetime.now().isoformat(),
        "areas": areas_procesadas
    }
    os.makedirs(
        os.path.dirname(FLAG_PATH),
        exist_ok=True
    )
    with open(FLAG_PATH, "w", encoding="utf-8") as f:
       
        json.dump(contenido, f, ensure_ascii=False, indent=2)

    logger.info("🚩 Flag creado para KNIME")

def borrar_flag():
    if os.path.exists(FLAG_PATH):
        os.remove(FLAG_PATH)

#ntfy notificaciones --------------------------------------
def notificar(mensaje):
    try:
        requests.post(
            "https://ntfy.sh/toaahora_wathdog_9f3k",
            data=mensaje.encode("utf-8")
        )
    except:
        pass
    



def limpiar_temporales():

    logger.info("🧹 Limpiando temporales...")

    extensiones_basura = [
        ".crdownload",
        ".tmp"
    ]

    tiempo_limite = 60 * 10  # 10 minutos

    ahora = time.time()

    carpetas = [
        DOWNLOAD_PATH
    ]

    for carpeta in carpetas:

        if not os.path.exists(carpeta):
            continue

        for archivo in os.listdir(carpeta):

            ruta = os.path.join(carpeta, archivo)

            try:

                # 🔥 extensión temporal
                if any(archivo.endswith(ext) for ext in extensiones_basura):

                    tiempo_archivo = os.path.getmtime(ruta)

                    if (ahora - tiempo_archivo) > tiempo_limite:

                        os.remove(ruta)

                        logger.info(f"🗑 Eliminado temporal: {archivo}")

                # 🔥 archivo vacío/corrupto
                elif archivo.endswith(".xlsx"):

                    if os.path.getsize(ruta) == 0:

                        os.remove(ruta)

                        logger.info(f"🗑 Eliminado corrupto: {archivo}")

            except Exception as e:
                
                logger.warning(f"⚠ Error limpiando {archivo}: {e}")
                
                
def guardar_screenshot(driver, nombre="error"):

    carpeta = "screenshots"

    os.makedirs(carpeta, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    ruta = os.path.join(
        carpeta,
        f"{nombre}_{timestamp}.png"
    )

    try:

        driver.save_screenshot(ruta)

        print(f"📸 Screenshot guardado: {ruta}")

        return ruta

    except Exception as e:

        print(f"⚠ Error guardando screenshot: {e}")

        return None
    
    
def entregar_archivos_finales():

    print("📦 Entregando archivos finales a KNIME...")

    os.makedirs(DESTINO, exist_ok=True)

    archivos = [

        f for f in os.listdir(PROCESSED_PATH)

        if f.endswith(".xlsx")
    ]

    if not archivos:

        print("⚠ No hay archivos para entregar")

        return

    for archivo in archivos:

        origen = os.path.join(
            PROCESSED_PATH,
            archivo
        )

        destino = os.path.join(
            DESTINO,
            archivo
        )

        try:

            # 🔥 eliminar archivo anterior
            if os.path.exists(destino):

                os.remove(destino)

            shutil.move(
                origen,
                destino
            )

            print(f"✅ Entregado: {archivo}")

        except Exception as e:

            print(
                f"❌ Error entregando "
                f"{archivo}: {e}"
            )
            
def limpiar_screenshots():

    carpeta = "screenshots"

    if not os.path.exists(carpeta):
        return

    for archivo in os.listdir(carpeta):

        if archivo.endswith(".png"):

            try:
                os.remove(
                    os.path.join(carpeta, archivo)
                )
            except:
                pass
            
            
RUNTIME_PATH = os.path.join(
    "data",
    "runtime.json"
)

def actualizar_runtime(segundos=300):

    proximo = time.time() + segundos

    data = {
        "next_run": proximo
    }

    with open(RUNTIME_PATH, "w") as f:

        json.dump(data, f)
        
def obtener_runtime():

    try:

        with open(RUNTIME_PATH, "r") as f:

            return json.load(f)

    except:

        return {}
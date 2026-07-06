import json
import os

COMMANDS_PATH = r"C:\Users\adolf\OneDrive\Escritorio\github\agente_monitor\commands.json"


def obtener_comando(nombre_bot):

    try:

        if not os.path.exists(
            COMMANDS_PATH
        ):

            return None

        with open(
            COMMANDS_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return data.get(
            nombre_bot
        )

    except:

        return None
    
def eliminar_comando(nombre_bot):

    try:

        with open(
            COMMANDS_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        if nombre_bot in data:

            del data[nombre_bot]

        with open(
            COMMANDS_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    except:

        pass

def procesar_comandos():

    comando = obtener_comando(
        "TOA"
    )

    if not comando:

        return False

    accion = comando.get(
        "accion"
    )

    print(
        f"📨 Comando recibido: {accion}"
    )

    if accion == "REINICIAR":

        eliminar_comando(
            "TOA"
        )

        return True

    return False
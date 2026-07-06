import json

from datetime import datetime

from bot_state import BOT_STATE

HEARTBEAT_PATH = "data/estado.json"

def guardar_estado():

    BOT_STATE["ultima_actualizacion"] = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    with open(
        HEARTBEAT_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            BOT_STATE,
            f,
            ensure_ascii=False,
            indent=4
        )


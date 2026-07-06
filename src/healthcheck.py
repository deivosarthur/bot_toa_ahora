import json
from datetime import datetime

STATE_PATH = "data/estado.json"


def bot_esta_caido():

    try:

        with open(STATE_PATH, "r") as f:
            data = json.load(f)

        heartbeat = datetime.strptime(
            data["ultimo_heartbeat"],
            "%Y-%m-%d %H:%M:%S"
        )

        diferencia = datetime.now() - heartbeat

        # 🔥 si pasan más de 5 minutos
        return diferencia.total_seconds() > 180

    except:
        return True
# config/config.py
DOWNLOAD_PATH = "data/downloads"
import os

DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOWNLOAD_PATH = os.path.join(BASE_DIR, "data", "downloads")

DESTINO = r"C:\temp\Toa_ahora\temp"

DESTINO_HISTORICO = r"C:\temp\Toa_ahora\NewTemp"

FLAG_PATH = r"C:\_TG_\Bots\bot_toa_ahora\flags\TOA_OK.flag"

PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")

STATE_PATH = os.path.join(BASE_DIR, "data", "estado.json")

META_PATH = os.path.join(BASE_DIR, "data", "last_run.json")

DESTINO = r"C:\temp\Toa_ahora\temp"
DESTINO_HISTORICO = r"C:\temp\Toa_ahora\NewTemp"

FLAG_PATH = r"C:\_TG_\Bots\bot_toa_ahora\flags\TOA_OK.flag"
prefs = {
    "download.default_directory": r"C:\Users\Bots2\Downloads"
}
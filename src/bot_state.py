from datetime import datetime

BOT_STATE = {
    "bot": "TOA",
    "version": "2.0",

    "estado": "INICIANDO",
    "mensaje": "",

    "ultima_actualizacion": "",
    "ultima_descarga": "",

    "ciclos_ok": 0,
    "errores": 0,
    "reinicios": 0,

    "errores_consecutivos": 0,
    "alerta_error_enviada": False,

    "uptime_inicio":
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    "pid_bot": 2780,
    "pid_chromedriver": 19948,
    "pid_chrome": 7876
        
}
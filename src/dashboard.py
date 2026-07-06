
from flask import Flask, send_from_directory
from datetime import datetime
import os
import json
from db import contar_descargas_hoy
import time

from db import (
    contar_descargas,
    obtener_descargas,
    obtener_stats_areas
)
from file_manager import obtener_runtime
from file_manager import BOT_START

app = Flask(__name__)


# =========================================
# HELPERS
# =========================================
def get_countdown():

    runtime = obtener_runtime()

    next_run = runtime.get("next_run")

    if not next_run:
        return "--:--"

    restante = int(next_run - time.time())

    if restante < 0:
        restante = 0

    minutos = restante // 60

    segundos = restante % 60

    return f"{minutos:02}:{segundos:02}"


def get_estado():

    try:
        with open("data/estado.json", "r") as f:
            return json.load(f)

    except:
        return {
            "estado": "DESCONOCIDO",
            "ultima_ejecucion": "-"
        }


def get_logs(limit=20):

    try:
        with open("logs/bot.log", "r", encoding="utf-8") as f:
            lines = f.readlines()

        return lines[-limit:]

    except:
        return ["No hay logs"]


def obtener_ultimo_screenshot():

    carpeta = "screenshots"

    if not os.path.exists(carpeta):
        return None

    archivos = [
        f for f in os.listdir(carpeta)
        if f.endswith(".png")
    ]

    if not archivos:
        return None

    ultimo = max(
        archivos,
        key=lambda x: os.path.getctime(
            os.path.join(carpeta, x)
        )
    )

    return ultimo


# =========================================
# RUTAS
# =========================================

@app.route('/logs')
def logs_completos():

    try:

        with open(
            'logs/bot.log',
            'r',
            encoding='utf-8'
        ) as f:

            contenido = f.read()

    except:

        contenido = 'No logs'

    return f"""
    <html>
    <body style='
        background:#0f172a;
        color:white;
        font-family:monospace;
        padding:20px;
    '>

    <h1>📜 Logs completos</h1>

    <pre>{contenido}</pre>

    </body>
    </html>
    """


@app.route("/")
def home():
    countdown = get_countdown()
    estado = get_estado()

    rows = obtener_descargas()

    total = contar_descargas_hoy()

    stats = obtener_stats_areas()

    logs = get_logs()

    uptime = datetime.now() - BOT_START

    ultimo_screenshot = obtener_ultimo_screenshot()

    html = f"""
    <html>

    <head>

        <title>BOT TOA DASHBOARD</title>

        <meta http-equiv="refresh" content="30">

        <style>

            body {{
                background: #0f172a;
                color: white;
                font-family: Arial;
                margin: 0;
                padding: 0;
            }}

            .header {{
                background: #111827;
                padding: 20px;
                text-align: center;
                border-bottom: 2px solid #334155;
            }}

            .header h1 {{
                margin: 0;
            }}

            .container {{
                width: 95%;
                margin: auto;
                padding: 20px;
            }}

            .cards {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: center;
                margin-bottom: 30px;
            }}

            .card {{
                background: #1e293b;
                padding: 20px;
                border-radius: 12px;
                min-width: 220px;
                text-align: center;
                box-shadow: 0 0 10px rgba(0,0,0,0.3);
            }}

            .card h2 {{
                color: #3b82f6;
                margin-bottom: 10px;
            }}

            .card p {{
                font-size: 22px;
                margin: 0;
            }}

            .green {{
                color: #22c55e;
            }}

            .red {{
                color: #ef4444;
            }}

            .section {{
                background: #111827;
                margin-bottom: 30px;
                padding: 20px;
                border-radius: 12px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th {{
                background: #3b82f6;
                padding: 12px;
            }}

            td {{
                border: 1px solid #334155;
                padding: 10px;
                text-align: center;
            }}

            tr:hover {{
                background: #1e293b;
            }}

            .log-box {{
                background: #0b1220;
                padding: 10px;
                margin-bottom: 8px;
                border-left: 5px solid #22c55e;
                font-family: monospace;
                border-radius: 5px;
            }}

            .error {{
                border-left: 5px solid #ef4444;
            }}

            .screenshot {{
                text-align: center;
            }}

            .screenshot img {{
                width: 90%;
                border-radius: 12px;
                border: 2px solid #334155;
                margin-top: 20px;
            }}

            .actions {{
                text-align: center;
                margin-bottom: 30px;
            }}

            .actions button {{
                padding: 15px 25px;
                font-size: 16px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                margin: 5px;
                color: white;
            }}

            .btn-restart {{
                background: #ef4444;
            }}

            .btn-clean {{
                background: #3b82f6;
            }}

        </style>

    </head>

    <body>

        <div class="header">
            <h1>🤖 BOT TOA DASHBOARD</h1>
            <p>Monitoreo en tiempo real</p>
        </div>

        <div class="container">

            <!-- CARDS -->
            <div class="cards">

                <div class="card">
                    <h2>Estado</h2>
                    <p class="green">{estado['estado']}</p>
                </div>

                <div class="card">
                    <h2>Total Descargas</h2>
                    <p>{total}</p>
                </div>

                <div class="card">
                    <h2>Última ejecución</h2>
                    <p>{estado['ultima_ejecucion']}</p>
                </div>
                <div class="card">
                    <h2>Próximo ciclo</h2>
                    <p>{countdown}</p>
                </div>

                <div class="card">
                    <h2>Uptime</h2>
                    <p>{str(uptime).split('.')[0]}</p>
                </div>

            </div>

            <!-- BOTONES -->
            <div class="actions">

                <a href="/reiniciar">
                    <button class="btn-restart">
                        🔄 Reiniciar Bot
                    </button>
                </a>

                <a href="/limpiar">
                    <button class="btn-clean">
                        🧹 Limpiar temporales
                    </button>
                </a>
                    <a href="/logs" target="_blank">
    <button class="btn-clean">
        📜 Ver logs completos
    </button>
</a>
            </div>

            <!-- STATS -->
            <div class="section">

                <h2>📊 Descargas por área</h2>

                <div class="cards">
            """

    for s in stats:

        html += f"""
        <div class="card">
            <h2>{s[0]}</h2>
            <p>{s[1]}</p>
        </div>
        """

    html += """
                </div>
            </div>

            <!-- SCREENSHOT -->
            <div class="section screenshot">

                <h2>📸 Último Screenshot Error</h2>
    """

    if ultimo_screenshot:

        html += f"""
        <img src="/screenshots/{ultimo_screenshot}">
        """

    else:

        html += """
        <p>No hay screenshots registrados</p>
        """

    html += """
            </div>

            <!-- LOGS -->
            <div class="section">

                <h2>📜 Logs en vivo</h2>
    """

    for log in logs:

        css = "log-box"

        if "ERROR" in log:
            css += " error"

        html += f"""
        <div class="{css}">
            {log}
        </div>
        """

    html += """
            </div>

            <!-- TABLA -->
            <div class="section">

                <h2>📁 Últimas descargas</h2>

                <table>

                    <tr>
                        <th>Área</th>
                        <th>Archivo</th>
                        <th>Fecha</th>
                        <th>Estado</th>
                    </tr>
    """

    for r in rows:

        html += f"""
        <tr>
            <td>{r[0]}</td>
            <td>{r[1]}</td>
            <td>{r[2]}</td>
            <td>{r[3]}</td>
        </tr>
        """

    html += """
                </table>

            </div>

        </div>

    </body>

    </html>
    """

    return html


@app.route('/screenshots/<path:filename>')
def screenshots(filename):

    return send_from_directory(
        '../screenshots',
        filename
    )


if __name__ == '__main__':
    app.run(port=5000)


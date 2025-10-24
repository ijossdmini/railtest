import requests
from bs4 import BeautifulSoup
import time
import os

# --- Variables de entorno ---
TOKEN = os.getenv("8016740350:AAFGA3qGe7PR06J6lNrfi5nFbf15BZtAOy4")
CHAT_ID = os.getenv("1521569191")
URL_NEQUI = "https://www.nequi.com.co/status"
INTERVALO = 120  # segundos entre revisiones
ultima_estado = None

def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": texto})
    except Exception as e:
        print("Error al enviar mensaje:", e)

def obtener_estado():
    try:
        r = requests.get(URL_NEQUI, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        estado_texto = soup.get_text().lower()
        return estado_texto
    except Exception as e:
        print("Error al leer la página:", e)
        return None

print("🤖 Monitor Nequi en ejecución...")
enviar_mensaje("📡 Monitor de estado Nequi activado en Railway.")

while True:
    estado_actual = obtener_estado()
    if estado_actual:
        if ultima_estado is None:
            ultima_estado = estado_actual
        elif estado_actual != ultima_estado:
            if any(palabra in estado_actual for palabra in ["operativa", "funcionando", "normal", "sin fallas"]):
                enviar_mensaje("✅ ¡Nequi ya está funcionando correctamente!")
            elif any(palabra in estado_actual for palabra in ["caído", "problema", "falla", "intermitencia"]):
                enviar_mensaje("🚨 Nequi presenta fallas nuevamente.")
            ultima_estado = estado_actual

    time.sleep(INTERVALO)
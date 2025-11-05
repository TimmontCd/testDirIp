from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
import requests
import logging
logging.basicConfig(level=logging.INFO)
from fastapi.responses import JSONResponse

load_dotenv()
app = FastAPI()

BACKEND_URL = os.getenv("BACKEND_URL")
HEADERS = {
    "X-IBM-Client-Id": os.getenv("CLIENT_ID"),
    "X-IBM-Client-Secret": os.getenv("CLIENT_SECRET"),
    "X-Request-Channel": os.getenv("CHANNEL"),
    "X-Request-UserExecute": os.getenv("USER_EXECUTE"),
    "cache-control": "no-cache",
    "ngrok-skip-browser-warning": "true"  # ← esta línea es clave
}


@app.post("/api/messages")
async def handle_message(request: Request):
    payload = await request.json()
    headers = dict(request.headers)

    logging.info(f"📨 Payload recibido: {payload}")
    logging.info(f"🧾 Headers recibidos: {headers}")

    params = {
        "searchType": "F",
        "informationSearch": payload.get("search", "")
    }

    try:
        logging.info(f"🔁 Orquestando llamada al backend:")
        logging.info(f"🔗 URL: {BACKEND_URL}")
        logging.info(f"🧾 Headers: {HEADERS}")
        logging.info(f"📦 Parámetros: {params}")

        response = requests.get(BACKEND_URL, headers=HEADERS, params=params)
        return JSONResponse(
            content=response.json(),
            headers={"ngrok-skip-browser-warning": "true"}  # ← aquí está la clave
        )
    except Exception as e:
        logging.error(f"❌ Error en la llamada al backend: {e}")
        return {"error": str(e)}


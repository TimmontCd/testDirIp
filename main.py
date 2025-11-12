from fastapi import FastAPI, Request
from fastmcp import FastMCP
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import requests
import logging
import os

# Configurar logs
logging.basicConfig(level=logging.INFO)

# Cargar variables de entorno
load_dotenv()

# Crear app y servidor MCP
app = FastAPI()
mcp = FastMCP(app, name="search-mcp-server", version="1.0.0")

# Variables del backend
BACKEND_URL = os.getenv("BACKEND_URL")
HEADERS = {
    "X-IBM-Client-Id": os.getenv("CLIENT_ID"),
    "X-IBM-Client-Secret": os.getenv("CLIENT_SECRET"),
    "X-Request-Channel": os.getenv("CHANNEL"),
    "X-Request-UserExecute": os.getenv("USER_EXECUTE"),
    "cache-control": "no-cache",
    "ngrok-skip-browser-warning": "true"
}

# Modelo del request
class SearchPayload(BaseModel):
    search: str


# 🔹 Endpoint REST tradicional (mantienes compatibilidad con tus integraciones actuales)
@app.post("/api/messages")
async def handle_message(payload: SearchPayload, request: Request):
    headers = dict(request.headers)
    logging.info(f"📨 Payload recibido: {payload}")
    logging.info(f"🧾 Headers recibidos: {headers}")

    params = {
        "searchType": "F",
        "informationSearch": payload.search
    }

    try:
        logging.info(f"🔁 Llamando backend {BACKEND_URL}")
        response = requests.get(BACKEND_URL, headers=HEADERS, params=params)
        return JSONResponse(content=response.json())
    except Exception as e:
        logging.error(f"❌ Error en backend: {e}")
        return {"error": str(e)}


# 🔹 Recurso MCP
@mcp.resource("search")
async def search_resource():
    return {
        "id": "search",
        "name": "Search Resource",
        "description": "Consulta texto libre contra el backend",
        "type": "query"
    }


# 🔹 Herramienta MCP — sin input_schema (FastMCP 0.4.1 lo detecta automáticamente)
@mcp.tool("search-tool")
async def search_tool(search: str):
    """Ejecuta búsquedas en el backend"""
    params = {
        "searchType": "F",
        "informationSearch": search
    }
    try:
        logging.info(f"🔍 Ejecutando MCP search con término: {search}")
        response = requests.get(BACKEND_URL, headers=HEADERS, params=params)
        return response.json()
    except Exception as e:
        logging.error(f"❌ Error MCP backend: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



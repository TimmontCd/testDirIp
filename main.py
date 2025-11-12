import os
import logging
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from mcp.server.fastmcp import FastMCP

# Configuración inicial
logging.basicConfig(level=logging.INFO)
load_dotenv()

# Inicialización del servidor MCP
app = FastAPI()
mcp = FastMCP("search-tool-server")

# Variables de entorno y configuración del backend
BACKEND_URL = os.getenv("BACKEND_URL")
HEADERS = {
    "X-IBM-Client-Id": os.getenv("CLIENT_ID"),
    "X-IBM-Client-Secret": os.getenv("CLIENT_SECRET"),
    "X-Request-Channel": os.getenv("CHANNEL"),
    "X-Request-UserExecute": os.getenv("USER_EXECUTE"),
    "cache-control": "no-cache",
    "ngrok-skip-browser-warning": "true"
}

# Herramienta MCP: búsqueda de clientes
@mcp.tool()
async def search_tool(search: str) -> dict:
    """
    Herramienta MCP que ejecuta búsquedas de texto libre contra el backend.
    """
    params = {"searchType": "F", "informationSearch": search}

    try:
        logging.info(f"🔍 Ejecutando MCP search con término: {search}")

        async with httpx.AsyncClient(headers=HEADERS, timeout=30.0) as client:
            response = await client.get(BACKEND_URL, params=params)
            response.raise_for_status()
            return response.json()

    except httpx.RequestError as e:
        logging.error(f"❌ Error MCP backend: {e}")
        return {"error": f"Error al consultar el backend: {e}"}

# Endpoint raíz para verificar que el servicio está vivo
@app.get("/")
def root():
    return {"status": "ok", "server": "search-tool-server"}

# Punto de entrada principal para Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

import os
import httpx
import logging
from dotenv import load_dotenv
from fastmcp import FastMCP, MCPTool, MCPResource

# Configuración de logging y variables de entorno
logging.basicConfig(level=logging.INFO)
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CHANNEL = os.getenv("CHANNEL")
USER_EXECUTE = os.getenv("USER_EXECUTE")

if not BACKEND_URL:
    raise RuntimeError("❌ BACKEND_URL no está configurado en .env")

BASE_HEADERS = {
    "X-IBM-Client-Id": CLIENT_ID or "",
    "X-IBM-Client-Secret": CLIENT_SECRET or "",
    "X-Request-Channel": CHANNEL or "",
    "X-Request-UserExecute": USER_EXECUTE or "",
    "cache-control": "no-cache",
    "ngrok-skip-browser-warning": "true"
}

# Inicializa servidor MCP
app = FastMCP(
    name="search-mcp-server",
    version="1.0.0",
    description="Servidor MCP que expone recursos y herramientas de búsqueda"
)

# --- RESOURCE: search ---
@app.resource("search")
class SearchResource(MCPResource):
    """Consulta de información en backend por texto"""

    async def on_query(self, query: str):
        params = {"searchType": "F", "informationSearch": query}
        logging.info(f"🔍 Realizando búsqueda para: {query}")
        async with httpx.AsyncClient() as client:
            resp = await client.get(BACKEND_URL, headers=BASE_HEADERS, params=params, timeout=30.0)
            return resp.json()


# --- TOOL: search-tool ---
@app.tool("search-tool")
class SearchTool(MCPTool):
    """Ejecuta búsquedas en el backend"""

    input_schema = {
        "type": "object",
        "properties": {
            "search": {"type": "string"}
        },
        "required": ["search"]
    }

    async def handler(self, search: str):
        params = {"searchType": "F", "informationSearch": search}
        logging.info(f"🧰 Ejecutando herramienta MCP con parámetro: {search}")

        async with httpx.AsyncClient() as client:
            resp = await client.get(BACKEND_URL, headers=BASE_HEADERS, params=params, timeout=30.0)
            data = resp.json()

        return {
            "results": data,
            "count": len(data) if isinstance(data, list) else 1
        }


# --- Health check (opcional) ---
@app.health_check
async def health():
    return {"status": "ok"}


# --- Inicia el servidor MCP ---
if __name__ == "__main__":
    app.run(port=3000)

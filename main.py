import os
import httpx
import logging
from dotenv import load_dotenv
from fastmcp import FastMCP

# ======================================================
# CONFIGURACIÓN Y VARIABLES DE ENTORNO
# ======================================================
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

# ======================================================
# INICIALIZA EL SERVIDOR MCP
# ======================================================
app = FastMCP(
    name="search-mcp-server",
    version="1.0.0",
    description="Servidor MCP que realiza búsquedas de clientes en el backend"
)

# ======================================================
# TOOL: search-tool  → Mantiene la lógica de /api/messages
# ======================================================
@app.tool(
    "search-tool",
    description="Ejecuta búsquedas de clientes en el backend",
    input_schema={
        "type": "object",
        "properties": {
            "search": {"type": "string", "description": "Texto de búsqueda de cliente"}
        },
        "required": ["search"]
    }
)
async def search_tool(search: str):
    """
    Ejecuta la misma lógica que el endpoint /api/messages.
    """
    params = {"searchType": "F", "informationSearch": search}
    logging.info("📨 Ejecutando herramienta de búsqueda")
    logging.info(f"🔗 URL: {BACKEND_URL}")
    logging.info(f"🧾 Headers: {BASE_HEADERS}")
    logging.info(f"📦 Parámetros: {params}")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(BACKEND_URL, headers=BASE_HEADERS, params=params)
            resp.raise_for_status()
            data = resp.json()

        logging.info("✅ Respuesta recibida correctamente")
        return {"results": data, "ngrok-skip-browser-warning": "true"}

    except httpx.RequestError as e:
        logging.error(f"❌ Error de conexión al backend: {e}")
        return {"error": "No se pudo conectar con el backend", "details": str(e)}

    except httpx.HTTPStatusError as e:
        logging.error(f"❌ Error HTTP {e.response.status_code}: {e.response.text}")
        return {
            "error": f"HTTP {e.response.status_code}",
            "details": e.response.text
        }

# ======================================================
# RESOURCE: search → opcional (consulta directa)
# ======================================================
@app.resource(
    "search",
    description="Recurso que permite consultar texto libre contra el backend",
    input_schema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Texto libre de búsqueda"}
        },
        "required": ["query"]
    }
)
async def search_resource(query: str):
    """
    Igual que la herramienta, pero expuesto como recurso MCP.
    """
    logging.info(f"🔍 Recurso ejecutando búsqueda: {query}")
    params = {"searchType": "F", "informationSearch": query}

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(BACKEND_URL, headers=BASE_HEADERS, params=params)
        return resp.json()

# ======================================================
# HEALTH CHECK (opcional)
# ======================================================
@app.health_check
async def health():
    return {"status": "ok"}

# ======================================================
# PUNTO DE ENTRADA
# ======================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

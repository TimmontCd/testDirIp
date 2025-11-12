from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import logging
import httpx

logging.basicConfig(level=logging.INFO)
load_dotenv()

app = FastAPI(title="MCP Server - Search")

BACKEND_URL = os.getenv("BACKEND_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CHANNEL = os.getenv("CHANNEL")
USER_EXECUTE = os.getenv("USER_EXECUTE")

if not BACKEND_URL:
    raise RuntimeError("BACKEND_URL no está configurado en .env")

BASE_HEADERS = {
    "X-IBM-Client-Id": CLIENT_ID or "",
    "X-IBM-Client-Secret": CLIENT_SECRET or "",
    "X-Request-Channel": CHANNEL or "",
    "X-Request-UserExecute": USER_EXECUTE or "",
    "cache-control": "no-cache",
    "ngrok-skip-browser-warning": "true"
}

class SearchInput(BaseModel):
    search: str

from fastapi.responses import FileResponse

@app.get("/mcp.json")
async def get_manifest():
    return FileResponse("mcp.json", media_type="application/json")


@app.get("/health")
async def health():
    return {"status": "ok"}

# --- MCP: lista de recursos ---
@app.post("/resources/list")
async def resources_list():
    return {
        "resources": [
            {
                "id": "search",
                "name": "Search Resource",
                "description": "Consulta de información en backend por texto",
                "type": "query"
            }
        ]
    }

# --- MCP: consulta de recurso ---
@app.post("/resources/query")
async def resources_query(payload: SearchInput):
    params = {"searchType": "F", "informationSearch": payload.search}
    async with httpx.AsyncClient() as client:
        resp = await client.get(BACKEND_URL, headers=BASE_HEADERS, params=params, timeout=30.0)
    return JSONResponse(content=resp.json(), headers={"ngrok-skip-browser-warning": "true"})

# --- MCP: lista de herramientas ---
@app.post("/tools/list")
async def tools_list():
    return {
        "tools": [
            {
                "id": "search-tool",
                "name": "Search Tool",
                "description": "Ejecuta búsquedas en el backend",
                "inputSchema": {
                    "type": "object",
                    "properties": {"search": {"type": "string"}},
                    "required": ["search"]
                }
            }
        ]
    }

# --- MCP: ejecución de herramienta ---
@app.post("/tools/call")
async def tools_call(payload: dict, request: Request):
    tool_id = payload.get("toolId")
    args = payload.get("arguments", {})

    if tool_id != "search-tool":
        return JSONResponse(status_code=404, content={"error": "Tool not found"})

    search = args.get("search")
    if not search:
        return JSONResponse(status_code=400, content={"error": "Missing 'search' argument"})

    params = {"searchType": "F", "informationSearch": search}
    async with httpx.AsyncClient() as client:
        resp = await client.get(BACKEND_URL, headers=BASE_HEADERS, params=params, timeout=30.0)

    return JSONResponse(content=resp.json(), headers={"ngrok-skip-browser-warning": "true"})

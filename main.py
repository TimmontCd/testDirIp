import os
import json
import logging
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from mcp.server.fastmcp import FastMCP

# Config
logging.basicConfig(level=logging.INFO)
load_dotenv()

app = FastAPI()
mcp = FastMCP("search-tool-server")

BACKEND_URL = os.getenv("BACKEND_URL")
HEADERS = {
    "X-IBM-Client-Id": os.getenv("CLIENT_ID"),
    "X-IBM-Client-Secret": os.getenv("CLIENT_SECRET"),
    "X-Request-Channel": os.getenv("CHANNEL"),
    "X-Request-UserExecute": os.getenv("USER_EXECUTE"),
    "cache-control": "no-cache",
    "ngrok-skip-browser-warning": "true"
}

@mcp.tool()
async def search_tool(search: str) -> dict:
    params = {"searchType": "F", "informationSearch": search}
    try:
        logging.info(f"🔍 MCP search: {search}")
        async with httpx.AsyncClient(headers=HEADERS, timeout=30.0) as client:
            r = await client.get(BACKEND_URL, params=params)
            r.raise_for_status()
            return r.json()
    except httpx.RequestError as e:
        logging.error(f"❌ Backend error: {e}")
        return {"error": f"Error al consultar el backend: {e}"}

# Health
@app.get("/")
def root():
    return {"status": "ok", "server": "search-tool-server"}

# Manifest (sirve un archivo manifest.json que subes con tu repo)
@app.get("/manifest")
def manifest():
    path = os.path.join(os.path.dirname(__file__), "manifest.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return JSONResponse(content=data)

# JSON-RPC 2.0
@app.post("/rpc")
async def rpc(request: Request):
    req = await request.json()
    # Requerido: jsonrpc e id
    if req.get("jsonrpc") != "2.0" or "id" not in req or "method" not in req:
        return JSONResponse(
            status_code=400,
            content={"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32600, "message": "Invalid Request"}}
        )
    rid = req["id"]
    method = req["method"]
    params = req.get("params", {}) or {}

    try:
        if method == "tools/list":
            # Devuelve lista de herramientas disponibles
            tools = [
                {
                    "name": "search_tool",
                    "description": "Busca clientes en el backend por texto libre",
                    "parameters": {"search": {"type": "string", "description": "Texto a buscar"}},
                }
            ]
            return JSONResponse(content={"jsonrpc": "2.0", "id": rid, "result": {"tools": tools}})

        elif method == "tools/call":
            # Espera: {"name": "...", "arguments": {...}}
            name = params.get("name")
            args = params.get("arguments", {}) or {}
            if name == "search_tool":
                result = await search_tool(**args)
                return JSONResponse(content={"jsonrpc": "2.0", "id": rid, "result": {"output": result}})
            else:
                return JSONResponse(
                    content={"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
                )
        else:
            return JSONResponse(
                content={"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
            )
    except Exception as e:
        logging.exception("RPC error")
        return JSONResponse(
            content={"jsonrpc": "2.0", "id": rid, "error": {"code": -32000, "message": str(e)}}
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

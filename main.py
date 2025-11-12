# main.py — HTTP fallback (recomendado)
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx, logging, os

logging.basicConfig(level=logging.INFO)
load_dotenv()

app = FastAPI(title="Search MCP (HTTP fallback)")

BACKEND_URL = os.getenv("BACKEND_URL")
HEADERS = {
    "X-IBM-Client-Id": os.getenv("CLIENT_ID"),
    "X-IBM-Client-Secret": os.getenv("CLIENT_SECRET"),
    "X-Request-Channel": os.getenv("CHANNEL"),
    "X-Request-UserExecute": os.getenv("USER_EXECUTE"),
    "cache-control": "no-cache",
}

class InvokePayload(BaseModel):
    search: str

@app.get("/mcp.json")
async def manifest():
    # Si existe manifest.json en la raíz, lo sirve; si no, devuelve inline (fallback)
    manifest_path = "mcp.json"
    if os.path.exists(manifest_path):
        return FileResponse(manifest_path, media_type="application/json")

@app.post("/invoke/search-tool")
async def invoke_search(payload: InvokePayload):
    params = {"searchType": "F", "informationSearch": payload.search}
    logging.info("Invocación search-tool payload=%s", payload.search)
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=30.0) as client:
            r = await client.get(BACKEND_URL, params=params)
            r.raise_for_status()
            return JSONResponse(content=r.json())
    except httpx.HTTPError as e:
        logging.error("HTTP error: %s", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
    except Exception as e:
        logging.error("Error general: %s", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)


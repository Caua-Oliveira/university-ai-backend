from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from src.api.routes import router as api_router
from src.core.config import settings

app = FastAPI(
    title="IA Universitária - Jorgina",
    description="API para o sistema de assistência universitária com Live2D",
    version="1.0.0"
)

# CORS Setup
# TODO: Restringir o acesso apenas para domínios confiáveis
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent.parent / "static"
STATIC_DIR.mkdir(exist_ok=True, parents=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


app.include_router(api_router, prefix="/api")

@app.get("/")
async def health_check():
    return {
        "status": "online",
        "message": "Jorgina está ouvindo.",
        "model": settings.MODEL_NAME
    }
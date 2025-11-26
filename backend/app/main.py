from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import asyncio
import logging
from dotenv import load_dotenv
import os

from .capture import PacketCapture
from .database import MongoDB
from .websocket_manager import ConnectionManager

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("capybara-ids")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage
    app.state.mongodb = MongoDB()
    app.state.ws_manager = ConnectionManager()
    app.state.packet_capture = PacketCapture(app.state.mongodb, app.state.ws_manager)
    
    # Démarrer la capture en arrière-plan
    asyncio.create_task(app.state.packet_capture.start_capture())
    
    yield
    
    # Nettoyage
    app.state.packet_capture.stop_capture()
    app.state.mongodb.close()

app = FastAPI(
    title="Capybara IDS",
    description="Système de Détection d'Intrusion Moderne",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes API
from .routes import alert, flows, stats, config

app.include_router(alert.router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(flows.router, prefix="/api/v1/flows", tags=["flows"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["stats"])
app.include_router(config.router, prefix="/api/v1/config", tags=["config"])
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await app.state.ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        app.state.ws_manager.disconnect(websocket)

@app.get("/")
async def root():
    return {"message": "Capybara IDS API", "status": "running"}
from fastapi import APIRouter, Request
from pydantic import BaseModel
import logging
import os

router = APIRouter()
logger = logging.getLogger("capybara-ids")

class ConfigUpdate(BaseModel):
    network_interface: str | None = None
    bpf_filter: str | None = None
    syn_flood_threshold: int | None = None
    port_scan_threshold: int | None = None
    ml_enabled: bool | None = None

@router.get("/")
async def get_config(request: Request):
    """Récupérer la configuration actuelle"""
    app = request.app
    return {
        'network_interface': os.getenv('NETWORK_INTERFACE', 'eth0'),
        'bpf_filter': os.getenv('BPF_FILTER', ''),
        'syn_flood_threshold': app.state.packet_capture.rule_detector.syn_flood_threshold,
        'port_scan_threshold': app.state.packet_capture.rule_detector.port_scan_threshold,
        'ml_enabled': app.state.packet_capture.ml_detector.is_ready()
    }

@router.post("/")
async def update_config(config: ConfigUpdate, request: Request):
    """Mettre à jour la configuration"""
    try:
        app = request.app
        
        if config.syn_flood_threshold is not None:
            app.state.packet_capture.rule_detector.syn_flood_threshold = config.syn_flood_threshold
        
        if config.port_scan_threshold is not None:
            app.state.packet_capture.rule_detector.port_scan_threshold = config.port_scan_threshold
        
        return {'message': 'Configuration mise à jour', 'success': True}
    except Exception as e:
        logger.error(f"Erreur mise à jour config: {e}")
        return {'message': str(e), 'success': False}

@router.post("/train")
async def train_model(request: Request):
    """Lancer l'entraînement du modèle ML"""
    try:
        from ..ml.train import IDSTrainer
        
        app = request.app
        trainer = IDSTrainer()
        
        X, y = trainer.load_data_from_mongodb(app.state.mongodb)
        
        if len(X) < 100:
            return {
                'success': False,
                'message': f'Pas assez de données ({len(X)} flows). Minimum 100 requis.'
            }
        
        if sum(y) > 10:
            metrics = trainer.train_random_forest(X, y)
        else:
            metrics = trainer.train_isolation_forest(X)
        
        model_path = trainer.save_model()
        
        app.state.packet_capture.ml_detector.load_model()
        
        return {
            'success': True,
            'message': 'Modèle entraîné avec succès',
            'metrics': metrics,
            'model_path': model_path
        }
        
    except Exception as e:
        logger.error(f"Erreur entraînement: {e}")
        return {
            'success': False,
            'message': str(e)
        }

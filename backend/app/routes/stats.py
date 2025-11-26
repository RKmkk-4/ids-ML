from fastapi import APIRouter
from datetime import datetime, timedelta
import logging
from ...app.main import app

router = APIRouter()

@router.get("/overview")
async def get_overview_stats(hours: int = 24):
    try:
        stats = await app.state.mongodb.get_flow_stats(hours)
        return stats
    except Exception as e:
        logging.error(f"Erreur statistiques overview: {e}")
        return {}

@router.get("/real-time")
async def get_real_time_stats():
    try:
        capture = app.state.packet_capture
        return {
            'packets_per_second': capture.stats['total_packets'] / 60 if capture.stats['total_packets'] > 0 else 0,
            'total_packets': capture.stats['total_packets'],
            'tcp_packets': capture.stats['tcp_packets'],
            'udp_packets': capture.stats['udp_packets'],
            'alerts': capture.stats['alerts'],
            'is_capturing': capture.is_capturing
        }
    except Exception as e:
        logging.error(f"Erreur stats temps réel: {e}")
        return {}
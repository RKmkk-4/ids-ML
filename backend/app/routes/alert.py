from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime, timedelta
import logging
from ...app.main import app

router = APIRouter()

@router.get("/")
async def get_alerts(
    limit: int = Query(100, ge=1, le=1000),
    severity: Optional[str] = None,
    type: Optional[str] = None
):
    try:
        query = {}
        if severity:
            query['severity'] = severity.upper()
        if type:
            query['type'] = {'$regex': type, '$options': 'i'}
        
        alerts = await app.state.mongodb.db.alerts.find(query) \
            .sort('timestamp', -1) \
            .limit(limit) \
            .to_list(length=limit)
        
        # Convertir ObjectId
        for alert in alerts:
            alert['_id'] = str(alert['_id'])
            
        return {
            'alerts': alerts,
            'total': len(alerts)
        }
    except Exception as e:
        logging.error(f"Erreur récupération alertes: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne")

@router.delete("/{alert_id}")
async def delete_alert(alert_id: str):
    try:
        from bson.objectid import ObjectId
        result = app.state.mongodb.db.alerts.delete_one({'_id': ObjectId(alert_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Alerte non trouvée")
        return {"message": "Alerte supprimée"}
    except Exception as e:
        logging.error(f"Erreur suppression alerte: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne")
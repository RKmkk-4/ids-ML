from fastapi import APIRouter, Query
from fastapi import Request
import logging

router = APIRouter()
logger = logging.getLogger("capybara-ids")

@router.get("/")
async def get_flows(
    request: Request,
    limit: int = Query(100, ge=1, le=1000),
    protocol: int | None = Query(None)
):
    """Récupérer les flows réseau"""
    try:
        app = request.app
        query: dict = {}
        if protocol:
            query['protocol'] = protocol
        
        flows = await app.state.mongodb.db.flows.find(query) \
            .sort('timestamp', -1) \
            .limit(limit) \
            .to_list(length=limit)
        
        for flow in flows:
            flow['_id'] = str(flow['_id'])
        
        return {
            'flows': flows,
            'total': len(flows)
        }
    except Exception as e:
        logger.error(f"Erreur récupération flows: {e}")
        return {'flows': [], 'total': 0}

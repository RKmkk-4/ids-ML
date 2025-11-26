from pymongo import MongoClient
from datetime import datetime, timedelta
import logging
import os

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Connexion à MongoDB"""
        try:
            mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
            self.client = MongoClient(mongodb_url)
            self.db = self.client.capybara_ids
            logging.info("Connecté à MongoDB avec succès")
        except Exception as e:
            logging.error(f"Erreur connexion MongoDB: {e}")
    
    def close(self):
        """Fermer la connexion"""
        if self.client:
            self.client.close()
    
    async def insert_flow(self, flow_data):
        """Insérer un flow réseau"""
        try:
            result = self.db.flows.insert_one(flow_data)
            return result.inserted_id
        except Exception as e:
            logging.error(f"Erreur insertion flow: {e}")
    
    async def insert_alert(self, alert_data):
        """Insérer une alerte"""
        try:
            result = self.db.alerts.insert_one(alert_data)
            return result.inserted_id
        except Exception as e:
            logging.error(f"Erreur insertion alerte: {e}")
    
    async def get_recent_alerts(self, limit=100):
        """Récupérer les alertes récentes"""
        try:
            alerts = list(self.db.alerts.find()
                         .sort('timestamp', -1)
                         .limit(limit))
            # Convertir ObjectId en string
            for alert in alerts:
                alert['_id'] = str(alert['_id'])
            return alerts
        except Exception as e:
            logging.error(f"Erreur récupération alertes: {e}")
            return []
    
    async def get_flow_stats(self, hours=24):
        """Statistiques des flows"""
        try:
            time_threshold = datetime.now() - timedelta(hours=hours)
            
            stats = {
                'total_flows': self.db.flows.count_documents({
                    'timestamp': {'$gte': time_threshold.isoformat()}
                }),
                'total_alerts': self.db.alerts.count_documents({
                    'timestamp': {'$gte': time_threshold.isoformat()}
                }),
                'alerts_by_severity': list(self.db.alerts.aggregate([
                    {'$match': {'timestamp': {'$gte': time_threshold.isoformat()}}},
                    {'$group': {'_id': '$severity', 'count': {'$sum': 1}}}
                ])),
                'top_source_ips': list(self.db.alerts.aggregate([
                    {'$match': {'timestamp': {'$gte': time_threshold.isoformat()}}},
                    {'$group': {'_id': '$src_ip', 'count': {'$sum': 1}}},
                    {'$sort': {'count': -1}},
                    {'$limit': 10}
                ]))
            }
            return stats
        except Exception as e:
            logging.error(f"Erreur statistiques: {e}")
            return {}
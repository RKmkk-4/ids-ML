import joblib
import numpy as np
import logging
from pathlib import Path

class MLDetector:
    def __init__(self):
        self.model = None
        self.features = None
        self.is_trained = False
        self.load_model()
    
    def load_model(self):
        """Charger le modèle ML pré-entraîné"""
        try:
            # Essayer de charger depuis le chemin configuré
            model_path = Path("backend/app/ml/models/random_forest.joblib")
            if model_path.exists():
                self.model = joblib.load(model_path)
                self.is_trained = True
                logging.info("Modèle ML chargé avec succès")
            else:
                logging.warning("Aucun modèle ML trouvé, création d'un modèle par défaut")
                self._create_dummy_model()
        except Exception as e:
            logging.error(f"Erreur chargement modèle: {e}")
            self._create_dummy_model()
    
    def _create_dummy_model(self):
        """Créer un modèle factice pour les tests"""
        from sklearn.ensemble import IsolationForest
        # Modèle simple pour démonstration
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False
    
    def is_ready(self):
        return self.is_trained and self.model is not None
    
    def detect(self, flow_data):
        """Détecter les anomalies avec le modèle ML"""
        if not self.is_ready():
            return None
        
        try:
            # Préparer les features pour le modèle
            features = self._extract_ml_features(flow_data)
            if features is None:
                return None
            
            # Prédiction
            prediction = self.model.predict([features])
            anomaly_score = self.model.decision_function([features])[0]
            
            # Si anomalie détectée
            if prediction[0] == -1 or anomaly_score < -0.1:
                return {
                    'type': 'ML Anomaly',
                    'severity': 'HIGH' if anomaly_score < -0.2 else 'MEDIUM',
                    'src_ip': flow_data['src_ip'],
                    'description': f'Anomalie détectée par ML (score: {anomaly_score:.3f})',
                    'confidence': abs(anomaly_score)
                }
                
        except Exception as e:
            logging.error(f"Erreur prédiction ML: {e}")
        
        return None
    
    def _extract_ml_features(self, flow_data):
        """Extraire et normaliser les features pour le modèle ML"""
        try:
            features = [
                flow_data.get('length', 0),
                flow_data.get('ttl', 64),
                flow_data.get('src_port', 0) % 1000,  # Normalisation
                flow_data.get('dst_port', 0) % 1000,
                1 if flow_data.get('protocol') == 6 else 0,  # TCP
                1 if flow_data.get('protocol') == 17 else 0, # UDP
                len(flow_data.get('flags', ''))
            ]
            return features
        except Exception as e:
            logging.error(f"Erreur extraction features: {e}")
            return None
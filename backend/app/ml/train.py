import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger("ml-training")

class IDSTrainer:
    """Pipeline d'entraînement pour les modèles IDS"""
    
    def __init__(self):
        self.model = None
        self.model_type = None
        self.model_dir = Path("backend/app/ml/models")
        self.model_dir.mkdir(parents=True, exist_ok=True)
    
    def load_data_from_mongodb(self, mongodb):
        """Charger les données depuis MongoDB"""
        logger.info("Chargement des données depuis MongoDB...")
        
        flows = list(mongodb.db.flows.find().limit(10000))
        alerts = list(mongodb.db.alerts.find())
        
        malicious_ips = set()
        for alert in alerts:
            if 'src_ip' in alert:
                malicious_ips.add(alert['src_ip'])
        
        data = []
        labels = []
        
        for flow in flows:
            features = self._extract_features(flow)
            if features is not None:
                data.append(features)
                labels.append(1 if flow.get('src_ip') in malicious_ips else 0)
        
        logger.info(f"Chargé {len(data)} flows, {sum(labels)} malveillants")
        return np.array(data), np.array(labels)
    
    def load_data_from_csv(self, filepath):
        """Charger depuis un dataset CSV (ex: NSL-KDD, CICIDS2017)"""
        logger.info(f"Chargement depuis {filepath}...")
        
        df = pd.read_csv(filepath)
        
        feature_cols = ['length', 'ttl', 'src_port', 'dst_port', 
                       'protocol_tcp', 'protocol_udp', 'flags_count']
        
        X = df[feature_cols].values
        y = (df['label'] != 'normal').astype(int).values
        
        logger.info(f"Chargé {len(X)} samples, {sum(y)} attaques")
        return X, y
    
    def _extract_features(self, flow):
        """Extraire features ML depuis un flow MongoDB"""
        try:
            return [
                flow.get('length', 0),
                flow.get('ttl', 64),
                flow.get('src_port', 0) % 1000,
                flow.get('dst_port', 0) % 1000,
                1 if flow.get('protocol') == 6 else 0,
                1 if flow.get('protocol') == 17 else 0,
                len(flow.get('flags', ''))
            ]
        except Exception:
            return None
    
    def train_random_forest(self, X, y):
        """Entraîner un Random Forest Classifier"""
        logger.info("Entraînement Random Forest...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        self.model_type = 'random_forest'
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"Accuracy: {accuracy:.4f}")
        logger.info("Classification Report:")
        logger.info(f"\n{classification_report(y_test, y_pred)}")
        
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5)
        logger.info(f"CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        return {
            'accuracy': accuracy,
            'cv_accuracy': float(cv_scores.mean()),
            'cv_std': float(cv_scores.std())
        }
    
    def train_isolation_forest(self, X):
        """Entraîner un Isolation Forest (unsupervised)"""
        logger.info("Entraînement Isolation Forest...")
        
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X)
        self.model_type = 'isolation_forest'
        
        predictions = self.model.predict(X)
        anomaly_ratio = (predictions == -1).sum() / len(predictions)
        
        logger.info(f"Anomaly ratio: {anomaly_ratio:.4f}")
        
        return {
            'anomaly_ratio': float(anomaly_ratio)
        }
    
    def save_model(self):
        """Sauvegarder le modèle entraîné"""
        if self.model is None:
            raise ValueError("Aucun modèle à sauvegarder")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.model_type}_{timestamp}.joblib"
        filepath = self.model_dir / filename
        
        joblib.dump(self.model, filepath)
        logger.info(f"Modèle sauvegardé: {filepath}")
        
        default_path = self.model_dir / f"{self.model_type}.joblib"
        joblib.dump(self.model, default_path)
        logger.info(f"Modèle par défaut: {default_path}")
        
        return str(filepath)

if __name__ == "__main__":
    import sys
    from backend.app.database import MongoDB
    
    logging.basicConfig(level=logging.INFO)
    
    trainer = IDSTrainer()
    
    if len(sys.argv) > 1 and sys.argv[1] == "mongodb":
        mongodb = MongoDB()
        X, y = trainer.load_data_from_mongodb(mongodb)
        
        if len(X) > 100:
            metrics = trainer.train_random_forest(X, y)
        else:
            logger.warning("Pas assez de données labellisées, utilisation Isolation Forest")
            metrics = trainer.train_isolation_forest(X)
        
        trainer.save_model()
        mongodb.close()
    elif len(sys.argv) > 1:
        csv_path = sys.argv[1]
        X, y = trainer.load_data_from_csv(csv_path)
        metrics = trainer.train_random_forest(X, y)
        trainer.save_model()
    else:
        print("Usage:")
        print("  python -m backend.app.ml.train mongodb")
        print("  python -m backend.app.ml.train path/to/dataset.csv")

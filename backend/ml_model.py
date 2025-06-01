import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

class AsteroidClassifier:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = "../models/asteroid_classifier.joblib"
        
    def prepare_features(self, data):
        """Prepare features for model training or prediction"""
        features = [
            'diameter_min',
            'diameter_max',
            'velocity',
            'miss_distance'
        ]
        return data[features]
    
    def train(self, data):
        """Train the model using provided data"""
        X = self.prepare_features(data)
        y = data['is_hazardous']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.model.fit(X_train, y_train)
        
        # Save model
        if not os.path.exists("../models"):
            os.makedirs("../models")
        joblib.dump(self.model, self.model_path)
        
        return self.model.score(X_test, y_test)
    
    def predict(self, asteroid_data):
        """Make predictions for new asteroid data"""
        if self.model is None:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
            else:
                # Use a simple heuristic if no model is available
                risk_score = min(1.0, (
                    (asteroid_data['diameter_max'] / 50) * 0.4 +
                    (1 / (asteroid_data['miss_distance'] + 0.1)) * 0.4 +
                    (asteroid_data['velocity'] / 30) * 0.2
                ))
                return {
                    "is_hazardous": risk_score > 0.5,
                    "confidence": 0.7,
                    "risk_score": risk_score
                }
        
        X = self.prepare_features(pd.DataFrame([asteroid_data]))
        X_scaled = self.scaler.transform(X)
        
        # Get prediction and probability
        prediction = self.model.predict(X_scaled)[0]
        probability = self.model.predict_proba(X_scaled)[0]
        
        return {
            "is_hazardous": bool(prediction),
            "confidence": float(max(probability)),
            "risk_score": float(probability[1])  # Probability of being hazardous
        } 
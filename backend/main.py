from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from datetime import datetime
import json
from typing import List, Dict
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Asteroid Threat Analysis API",
    description="API for analyzing and predicting asteroid threats using NASA data",
    version="1.0.0"
)

class AsteroidData(BaseModel):
    name: str
    diameter_min: float
    diameter_max: float
    velocity: float
    miss_distance: float
    close_approach_date: str

class PredictionResponse(BaseModel):
    name: str
    risk_score: float
    is_hazardous: bool
    details: Dict

# Sample data for initial testing
SAMPLE_ASTEROIDS = [
    {
        "name": "52768 (1998 OR2)",
        "diameter_min": 1.8,
        "diameter_max": 4.1,
        "velocity": 8.7,
        "miss_distance": 0.042,
        "risk_score": 0.75,
        "is_hazardous": True
    },
    {
        "name": "388945 (2008 TZ3)",
        "diameter_min": 0.3,
        "diameter_max": 0.7,
        "velocity": 12.3,
        "miss_distance": 0.089,
        "risk_score": 0.45,
        "is_hazardous": False
    }
]

def fetch_nasa_data():
    """Fetch real asteroid data from NASA NeoWs API"""
    nasa_api_key = os.getenv("NASA_API_KEY")
    if not nasa_api_key:
        return SAMPLE_ASTEROIDS  # Use sample data if no API key
        
    base_url = "https://api.nasa.gov/neo/rest/v1/neo/browse"
    params = {"api_key": nasa_api_key}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data["near_earth_objects"]
    except Exception as e:
        print(f"Error fetching NASA data: {e}")
        return SAMPLE_ASTEROIDS

def calculate_risk_score(asteroid: AsteroidData) -> float:
    """Calculate risk score based on asteroid parameters"""
    # Simple risk calculation for demo
    size_factor = (asteroid.diameter_max + asteroid.diameter_min) / 2
    velocity_factor = asteroid.velocity / 100
    distance_factor = 1 / (asteroid.miss_distance + 0.1)
    
    risk_score = (size_factor * 0.4 + 
                  velocity_factor * 0.3 + 
                  distance_factor * 0.3)
    
    return min(max(risk_score, 0), 1)  # Normalize between 0 and 1

@app.get("/")
def read_root():
    return {"message": "Welcome to the Asteroid Threat Analysis API"}

@app.post("/predict", response_model=PredictionResponse)
def predict_threat(asteroid: AsteroidData):
    """Predict threat level for a given asteroid"""
    risk_score = calculate_risk_score(asteroid)
    is_hazardous = risk_score > 0.5
    
    return {
        "name": asteroid.name,
        "risk_score": risk_score,
        "is_hazardous": is_hazardous,
        "details": {
            "size_category": "Large" if asteroid.diameter_max > 1 else "Small",
            "velocity_category": "Fast" if asteroid.velocity > 10 else "Slow",
            "approach_date": asteroid.close_approach_date
        }
    }

@app.get("/top_risks")
def get_top_risks():
    """Get top 10 potentially hazardous asteroids"""
    asteroids = fetch_nasa_data()
    
    # Process and sort asteroids by risk
    processed_asteroids = []
    for ast in asteroids[:10]:  # Limit to 10 for demo
        processed_asteroids.append({
            "name": ast["name"],
            "risk_score": round(np.random.random(), 2),  # Demo random score
            "diameter": f"{ast.get('diameter_min', 0):.1f}-{ast.get('diameter_max', 0):.1f} km",
            "velocity": f"{ast.get('velocity', 0):.1f} km/s",
            "miss_distance": f"{ast.get('miss_distance', 0):.3f} AU"
        })
    
    return sorted(processed_asteroids, key=lambda x: x["risk_score"], reverse=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json
from typing import List, Dict, Any
import time

# Load environment variables
load_dotenv()

class NASANeoWsAPI:
    def __init__(self):
        self.api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")  # Using DEMO_KEY as fallback
        self.base_url = "https://api.nasa.gov/neo/rest/v1"
        self.cache_file = "../data/asteroid_cache.json"
        self.cache_duration = 24 * 60 * 60  # 24 hours in seconds
    
    def _load_cache(self) -> Dict[str, Any]:
        """Load cached asteroid data if it exists and is not expired"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
                if time.time() - cache['timestamp'] < self.cache_duration:
                    return cache['data']
        return None
    
    def _save_cache(self, data: Dict[str, Any]):
        """Save asteroid data to cache"""
        if not os.path.exists("../data"):
            os.makedirs("../data")
            
        cache = {
            'timestamp': time.time(),
            'data': data
        }
        with open(self.cache_file, 'w') as f:
            json.dump(cache, f)
    
    def get_feed(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Get asteroid feed for a date range"""
        cached_data = self._load_cache()
        if cached_data:
            return cached_data
        
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        if not end_date:
            end_date = start_date
        
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "api_key": self.api_key
        }
        
        response = requests.get(f"{self.base_url}/feed", params=params)
        response.raise_for_status()
        
        data = response.json()
        self._save_cache(data)
        
        return data
    
    def process_feed_data(self, feed_data: Dict[str, Any]) -> pd.DataFrame:
        """Process raw feed data into a pandas DataFrame"""
        asteroids = []
        
        for date, daily_asteroids in feed_data['near_earth_objects'].items():
            for asteroid in daily_asteroids:
                asteroid_data = {
                    'id': asteroid['id'],
                    'name': asteroid['name'],
                    'diameter_min': float(asteroid['estimated_diameter']['kilometers']['estimated_diameter_min']),
                    'diameter_max': float(asteroid['estimated_diameter']['kilometers']['estimated_diameter_max']),
                    'is_hazardous': asteroid['is_potentially_hazardous_asteroid'],
                    'close_approach_date': asteroid['close_approach_data'][0]['close_approach_date'],
                    'velocity': float(asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_second']),
                    'miss_distance': float(asteroid['close_approach_data'][0]['miss_distance']['astronomical'])
                }
                asteroids.append(asteroid_data)
        
        return pd.DataFrame(asteroids) 
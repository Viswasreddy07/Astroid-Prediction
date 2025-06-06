# 🛰 Asteroid Threat Analysis System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.2-red.svg)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--learn-orange.svg)

A sophisticated machine learning system that analyzes and predicts potential asteroid threats using NASA's Near Earth Object Web Service (NeoWs) API. The system features real-time data processing, machine learning-based threat assessment, and an interactive dashboard.

## 🌟 Key Features

- **Real-time NASA Data Integration**
  - Direct integration with NASA's NeoWs API
  - Automatic data caching to minimize API calls
  - Real-time asteroid tracking and monitoring

- **Advanced Threat Analysis**
  - Machine learning-based risk assessment
  - Multiple feature analysis (size, velocity, miss distance)
  - Confidence scoring for predictions

- **Interactive Dashboard**
  - Beautiful, animated UI with dark theme
  - Real-time metrics and visualizations
  - Interactive risk prediction interface
  - Top risk asteroids visualization

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance API framework
- **Scikit-learn**: Machine learning model implementation
- **Pandas**: Data processing and analysis
- **NASA NeoWs API**: Real-time asteroid data source

### Frontend
- **Streamlit**: Interactive dashboard
- **Plotly**: Dynamic data visualizations
- **Custom CSS**: Animated UI elements

### Data Management
- **Caching System**: Efficient data storage
- **JSON**: Data interchange format
- **JobLib**: Model persistence

## 📊 Features in Detail

### 1. Data Collection
- Automated NASA API integration
- Intelligent caching system
- Real-time data updates

### 2. Risk Analysis
- Feature engineering for asteroid characteristics
- Random Forest Classification model
- Probability-based risk scoring
- Confidence level assessment

### 3. User Interface
- Metric cards with real-time updates
- Interactive prediction form
- Dynamic risk visualization
- Animated alerts and notifications

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- NASA API key (get it from https://api.nasa.gov/)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/asteroid-threat-analysis.git
cd asteroid-threat-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory:
```env
NASA_API_KEY=your_api_key_here
```

### Running the Application

1. Start the backend server:
```bash
cd backend
python -m uvicorn main:app --reload
```

2. Launch the frontend (in a new terminal):
```bash
cd frontend
streamlit run streamlit_app.py
```

The application will be available at:
- Frontend Dashboard: http://localhost:8501
- API Documentation: http://localhost:8000/docs

## 📁 Project Structure

```
asteroid-threat-analysis/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── ml_model.py       # ML model implementation
│   └── nasa_api.py       # NASA API integration
├── frontend/
│   ├── streamlit_app.py  # Streamlit dashboard
│   └── style.css         # Custom styling
├── models/               # Saved ML models
├── data/                # Cached data
└── requirements.txt     # Project dependencies
```

## 🔧 API Endpoints

### `/predict`
- **Method**: POST
- **Purpose**: Get threat prediction for asteroid data
- **Input**: Asteroid characteristics (diameter, velocity, etc.)
- **Output**: Risk score and classification

### `/top_risks`
- **Method**: GET
- **Purpose**: Retrieve top 10 hazardous asteroids
- **Output**: List of highest risk asteroids

## 🎨 UI Components

1. **Header Section**
   - Project title with animated glow effect
   - Real-time status indicators

2. **Metrics Dashboard**
   - Active threats counter
   - Highest risk score
   - Next close approach timer

3. **Risk Analysis**
   - Interactive prediction form
   - Real-time risk assessment
   - Confidence scoring

4. **Visualization**
   - Risk distribution charts
   - Top threats bar chart
   - Animated alerts

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NASA NeoWs API for providing asteroid data
- Streamlit team for the amazing dashboard framework
- FastAPI team for the efficient backend framework

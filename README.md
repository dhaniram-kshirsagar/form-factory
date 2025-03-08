# 🏭 Foam Factory Data Intelligence Platform

## Overview
Foam Factory Data Intelligence is a comprehensive analytics and prediction platform for foam manufacturing operations. The application leverages machine learning models to provide insights into production metrics, maintenance needs, and operational efficiency.

## Key Features

### 📊 Interactive Dashboards
- Real-time monitoring of factory performance metrics
- Historical data analysis with customizable time ranges
- Multi-factory comparison capabilities

### 🔮 Predictive Analytics
- **Revenue Prediction**: Forecast future revenue with categorical filters (Product Category, Machine Type, Supplier)
- **Profit Margin Prediction**: Analyze expected profit margins with customizable filters
- **Production Volume Prediction**: Estimate upcoming production volumes with Raw Material Quality filters

### 🛠️ Predictive Maintenance
- Early detection of potential equipment failures
- Maintenance scheduling optimization
- Sensor data analysis and anomaly detection

### 🧠 Machine Learning Models
- Random Forest classifiers with hyperparameter tuning
- Comprehensive feature engineering pipeline
- Model evaluation metrics and visualization tools

## Installation & Setup

### Local Development

1. Clone the repository
   ```bash
   git clone https://github.com/dhaniram-kshirsagar/form-factory.git
   cd form-factory
   ```

2. Create and activate a virtual environment (recommended)
   ```bash
   python3 -m venv foamvenv
   source foamvenv/bin/activate  # On Windows: foamvenv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application
   ```bash
   streamlit run Home.py
   ```

### Production Deployment

1. Clone and setup environment
   ```bash
   git clone https://github.com/dhaniram-kshirsagar/form-factory.git
   python3 -m venv foamvenv
   source foamvenv/bin/activate
   pip install -r requirements.txt
   ```

2. Deploy as a background service
   ```bash
   nohup streamlit run Home.py &
   ```
   The application will be accessible at:
   - Local URL: http://localhost:8501
   - Network URL: http://<server-ip>:8501

3. For containerized deployment, use the provided Dockerfile (optional)

## Project Structure

```
form-factory/
├── app.py                  # Main application entry point
├── Home.py                 # Home page dashboard
├── modules/                # Core functionality modules
│   ├── data/               # Data processing and management
│   ├── ml/                 # Machine learning models
│   │   ├── predictor.py    # Prediction model implementations
│   │   ├── prediction.py   # Visualization of predictions
│   │   └── performance_pred.py # Performance prediction utilities
│   └── utils/              # Utility functions
├── page/                   # Streamlit page definitions
│   ├── Predictive_Performance.py # Predictive analytics dashboard
│   └── ...                 # Other application pages
├── models/                 # Saved ML model files
├── data/                   # Sample and historical data
└── config/                 # Configuration settings
```

## Usage Guide

1. **Home Dashboard**: View overall factory performance metrics
2. **Predictive Performance**: Access predictive analytics with the following features:
   - Select prediction type (Revenue, Profit Margin, Production Volume)
   - Apply categorical filters specific to each model
   - View time-series predictions with interactive charts
   - Analyze detailed prediction data tables

## Development

To extend the application with new models or features:

```bash
# Run the development server with auto-reload
streamlit run Home.py --server.runOnSave=true

# Train or update ML models
python -m modules.ml.train
```



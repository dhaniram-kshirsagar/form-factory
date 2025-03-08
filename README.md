# 🏭 Foam Factory Data Intelligence Platform

## Overview
Foam Factory Data Intelligence is a comprehensive analytics and prediction platform for foam manufacturing operations. The application leverages machine learning models and knowledge graph technology to provide insights into production metrics, maintenance needs, and operational efficiency.

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

### 🤖 Factory Bot
- AI-powered chatbot for querying factory data
- Natural language interface for complex data analysis
- Knowledge graph-based retrieval for accurate responses
- Caching mechanism with toggle functionality for improved performance
- Example questions for quick insights into factory operations
- RESTful API endpoints for headless integration

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
├── api.py                  # FastAPI backend for chatbot integration
├── Home.py                 # Home page dashboard
├── modules/                # Core functionality modules
│   ├── data/               # Data processing and management
│   ├── ml/                 # Machine learning models
│   │   ├── predictor.py    # Prediction model implementations
│   │   ├── prediction.py   # Visualization of predictions
│   │   └── performance_pred.py # Performance prediction utilities
│   ├── kg_rag/             # Knowledge Graph RAG components
│   │   ├── kg_rag.py       # Main RAG implementation
│   │   ├── cypher_prompt_template.py # Neo4j Cypher query templates
│   │   ├── qa_prompt_template.py # QA prompt templates
│   │   ├── cache.py        # Response caching system
│   │   ├── schema.cypher   # Knowledge graph schema definition
│   │   └── populate_neo4j.py # Database population utilities
│   └── utils/              # Utility functions
├── page/                   # Streamlit page definitions
│   ├── Predictive_Performance.py # Predictive analytics dashboard
│   ├── Factory_Bot.py      # AI chatbot interface
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
3. **Factory Bot**: Interact with the AI-powered assistant:
   - Ask natural language questions about factory data
   - Query complex relationships between machines, production, and performance
   - Analyze trends and patterns across different factories
   - Toggle cache functionality for improved performance
   - Use example questions for quick insights
   - View chat history with threaded conversation interface

## Development

To extend the application with new models or features:

```bash
# Run the development server with auto-reload
streamlit run Home.py --server.runOnSave=true

# Train or update ML models
python -m modules.ml.train

# Populate the knowledge graph database
python -m modules.kg_rag.populate_neo4j
```

## Knowledge Graph RAG System

The platform incorporates a Knowledge Graph Retrieval-Augmented Generation (RAG) system that enables natural language querying of complex factory data relationships:

- **Neo4j Backend**: Graph database storing factory data with relationships between entities
- **LLM Integration**: Combines graph queries with language model capabilities
- **Entity Schema**: Includes Factories, Machines, Teams, Members, Products, and more
- **Performance Optimization**: Implements caching for frequently asked questions

### API Integration

The platform provides a FastAPI backend for integrating the knowledge graph capabilities with external applications:

- **RESTful Endpoints**: `/chat` and `/cquery` for different query types
- **JSON Interface**: Simple request/response format for easy integration
- **CORS Support**: Configured for cross-origin requests

```python
# Example API usage with Python requests
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What is the average batch quality for each product category?"}
)
print(response.json())
```

### Environment Setup

To use the Knowledge Graph features and API, set up the following environment variables:

```bash
# .env file
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
API_HOST=localhost
API_PORT=8000
```


# 🏭 Foam Factory Data Intelligence

### How to run it on your own machine 🪟

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run Home.py
   ```


### Deploy it on lenode [NOTE following can be containerized as well] 💻

1. Checkout from github

> git clone https://github.com/dhaniram-kshirsagar/form-factory.git

2. Setup python venv

> python3 -m venv foamvenv
> source foamvenv/bin/activate

3. Install prerequisites

(foamvenv)> pip install -r requirements.txt

4. Now deploy streamlit form-factoy app

(foamvenv) > nohup streamlit run Home.py &

>>output

Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.


  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://<ip>:8501
  
  External URL: http://<ip>:8501

### Project Documentation

# Foam Factory Predictive Maintenance

## Overview
Machine learning system for predicting equipment failures in foam manufacturing equipment using sensor data and maintenance records.

## Features
- Data preprocessing pipeline
- Random Forest classifier with hyperparameter tuning
- Model evaluation metrics and visualization
- Production-ready configuration management

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run pipeline
python -m src.main
```

## Directory Structure
```
form-factory/
├── config/       # Configuration settings
├── data/         # Raw sensor data
├── models/       # Saved model files
├── src/          # Source code
└── output/       # Evaluation results

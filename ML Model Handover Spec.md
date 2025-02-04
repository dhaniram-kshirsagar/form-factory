# ML Model Handover Specification  
**Model Purpose**: Predict customer churn (Yes/No) for a telecom company.  

---

## 1. Files to Deliver  
- **Model File**: `churn_xgboost_model.pkl` (trained XGBoost classifier).  
- **Config File**: `feature_config.json` (feature names, scaler, and encoder mappings).  
- **Sample Dataset**: `sample_batch.csv` (10 rows with raw input schema).  
- **Inference Script**: `predict_churn.py` (supports single and CSV batch predictions).  
- **Requirements**: `requirements.txt` (Python dependencies).  

---

## 2. Inference Steps  

### Single Customer Prediction  
1. **Input**: A dictionary with raw customer data (e.g., `{"gender": "Female", "tenure": 5, ...}`).  
2. **Output**:  
   - `ChurnProbability` (float between 0–1).  
   - `ChurnStatus` ("Yes" or "No").  

### Batch Prediction (CSV File)  
1. **Input**: CSV file with raw customer data (same schema as training data).  
2. **Output**: CSV with two new columns:  
   - `ChurnProbability`: Probability of churn for each row.  
   - `ChurnStatus`: Predicted class ("Yes"/"No").  

---

## 3. Preprocessing Steps  

### Categorical Variables  
- **One-Hot Encoding**: Applied to `InternetService`, `PaymentMethod`, `Contract`, etc.  
  - Example: `PaymentMethod` → `PaymentMethod_CreditCard`, `PaymentMethod_ElectronicCheck`.  
- **Special Categories**: `No phone service`/`No internet service` treated as valid categories.  

### Numerical Variables  
- **Impute Missing Values**:  
  - `TotalCharges`: Replace missing values with median (stored in `feature_config.json`).  
- **Standard Scaling**: Applied to `tenure`, `MonthlyCharges`, `TotalCharges`.  

### Dropped Fields  
- **`customerID`**: Non-predictive identifier (removed during preprocessing).  

---

## 4. Sample Code for Batch Inference  

```python  
import pandas as pd  
import joblib  

# Load model, scaler, and config  
model = joblib.load("churn_xgboost_model.pkl")  
config = joblib.load("feature_config.json")  
scaler = config["scaler"]  
feature_order = config["feature_order"]  

# Load CSV batch file  
batch_df = pd.read_csv("input_batch.csv")  

# Preprocess data  
batch_df = batch_df.drop(columns=["customerID"], errors="ignore")  
batch_df["TotalCharges"] = batch_df["TotalCharges"].fillna(config["total_charges_median"])  

# One-Hot Encoding  
batch_encoded = pd.get_dummies(batch_df)  
batch_encoded = batch_encoded.reindex(columns=feature_order, fill_value=0)  

# Scale features  
batch_scaled = scaler.transform(batch_encoded)  

# Predict  
probabilities = model.predict_proba(batch_scaled)[:, 1]  
predictions = ["Yes" if prob > 0.5 else "No" for prob in probabilities]  

# Save output  
batch_df["ChurnProbability"] = probabilities  
batch_df["ChurnStatus"] = predictions  
batch_df.to_csv("output_predictions.csv", index=False)  

import pandas as pd
import joblib

# Load the preprocessed data
data = pd.read_csv("/Users/dhani/foamvenv/rev_model/preprocessed_data.csv")

# Load the trained model
model = joblib.load("/Users/dhani/foamvenv/rev_model/revenue_prediction_model.pkl")

# Select a sample of 5 rows
sample_data = data.sample(n=5, random_state=42)

# Drop the target variable (Revenue ($)) for prediction
X_sample = sample_data.drop(columns=["Revenue ($)"])

# Make predictions
predictions = model.predict(X_sample)

# Print predictions and probabilities
print("Sample Data:")
print(sample_data)
print("\nPredictions:")
print(predictions)
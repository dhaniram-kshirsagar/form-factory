import pandas as pd
import joblib

# Load the preprocessed data
data = pd.read_csv("preprocessed_data.csv")

# Load the trained model
model = joblib.load("prof_margin_prediction_model.pkl")

# Select a sample of 5 rows
sample_data = data.sample(n=5, random_state=42)
print(sample_data.columns)
# Drop the target variable (Revenue ($)) for prediction
X_sample = sample_data.drop(columns=["Profit Margin (%)"])

# Align features with training data
X_sample = X_sample[model.feature_names_in_]

# Make predictions
predictions = model.predict(X_sample)

# Print predictions and probabilities
print("Sample Data:")
print(sample_data)
print("\nPredictions:")
print(predictions)
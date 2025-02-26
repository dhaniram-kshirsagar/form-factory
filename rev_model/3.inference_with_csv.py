import pandas as pd
import joblib

# Load the preprocessed data
data = pd.read_csv("C:\\Users\\athar\\OneDrive\\Documents\\GitHub\\form-factory\\rev_model\\csvs\\preprocessed_data.csv")

# Load the trained model
model = joblib.load("C:\\Users\\athar\\OneDrive\\Documents\\GitHub\\form-factory\\rev_model\\revenue_prediction_model.pkl")

# Drop the target variable (Revenue ($)) for prediction
X = data.drop(columns=["Revenue ($)"])

# Make predictions
predictions = model.predict(X)

# Print predictions and probabilities
print("Predictions for all data:")
print(predictions)

# Get prediction probabilities (if model supports it)
try:
    probabilities = model.predict_proba(X)
    print("\nProbabilities:")
    print(probabilities)
except AttributeError:
    print("\nModel does not support probability predictions")

# Save predictions to CSV
predictions_df = data.copy()
predictions_df['Predicted Revenue ($)'] = predictions
try:
    predictions_df['Prediction Probability'] = probabilities[:, 1]  # Assuming binary classification
except NameError:
    pass
predictions_df.to_csv('C:\\Users\\athar\\OneDrive\\Documents\\GitHub\\form-factory\\rev_model\\csvs\\all_predictions.csv', index=False)


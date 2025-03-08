import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from pathlib import Path

PKL_PATH = Path(__file__).parent.parent/"modules/ml"/"revenue_prediction_model.pkl"
PROCESSED_CSV = Path(__file__).parent/"preprocessed_data.csv"
FEATURES_PATH = Path(__file__).parent/"imp_rev_features.md"
MEAN_VALUES_PATH = Path(__file__).parent/"mean_values.pkl"

# Load the preprocessed data
data = pd.read_csv(PROCESSED_CSV)

# Load the important features from imp_rev_features.md
with open(FEATURES_PATH, "r") as file:
    lines = file.readlines()
    important_features = [line.split("|")[1].strip() for line in lines[2:]]  # Skip header and footer

# Prepend month, year, Factory, and Location to the important features list
#important_features = ['month', 'year', 'Factory', 'Location'] + important_features

# Define features and target
X = data[important_features]
y = data["Revenue ($)"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models to evaluate
models = {
    "Random Forest": RandomForestRegressor(random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
    "Linear Regression": LinearRegression()
}

# Train and evaluate models
best_model = None
best_score = -float("inf")
best_model_name = ""

for name, model in models.items():
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"{name} - MSE: {mse}, R2: {r2}")
    
    # Track the best model
    if r2 > best_score:
        best_score = r2
        best_model = model
        best_model_name = name

# Save the best model to a .pkl file
joblib.dump(best_model, PKL_PATH)
print(f"Best model saved: {best_model_name} with R2 score: {best_score}")
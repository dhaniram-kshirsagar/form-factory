import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load the preprocessed data
data = pd.read_csv("preprocessed_data.csv")

# Load the important features from imp_prof_margin_features.md
with open("imp_prof_margin_features.md", "r") as file:
    lines = file.readlines()
    important_features = [line.split("|")[1].strip() for line in lines[2:]]  # Skip header and footer

# Define features and target
X = data[important_features]
y = data["Profit Margin (%)"]

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
joblib.dump(best_model, "prof_margin_prediction_model.pkl")
print(f"Best model saved: {best_model_name} with R2 score: {best_score}")
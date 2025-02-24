import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load the dataset
data = pd.read_csv("/Users/dhani/foamvenv/smart-data-intelligence/apps/foam_factory/modules/data/large-data/FoamFactory_V2_27K.csv")

# Define features and target
X = data.drop(columns=["Revenue ($)"])
y = data["Revenue ($)"]

# Convert categorical variables to dummy variables
X = pd.get_dummies(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor to determine feature importance
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Get feature importances
feature_importances = model.feature_importances_
feature_names = X.columns

# Create a DataFrame of feature importances
importance_df = pd.DataFrame({"Feature": feature_names, "Importance": feature_importances})

# Sort features by importance
importance_df = importance_df.sort_values(by="Importance", ascending=False)

# Select the top 10 most important features
top_features = importance_df.head(10)

# Save the top features to a markdown file
top_features.to_markdown("/Users/dhani/foamvenv/rev_model/imp_rev_features.md", index=False)
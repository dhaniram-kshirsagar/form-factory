import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import roc_auc_score, f1_score

# Load data
df = pd.read_csv("/Users/dhani/foamvenv/telecom_churn/form-factory/modules/data/telchurn/TelecomChurn.csv")

# Preprocessing
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())

X = df.drop(["customerID", "Churn"], axis=1)
y = df["Churn"].map({"Yes": 1, "No": 0})

# Encode categorical variables
cat_cols = X.select_dtypes(include="object").columns.tolist()
num_cols = X.select_dtypes(exclude="object").columns.tolist()

encoder = OneHotEncoder(drop="first", sparse=False)
X_encoded = pd.DataFrame(encoder.fit_transform(X[cat_cols]))
X_encoded.columns = encoder.get_feature_names_out(cat_cols)

# Combine features
X_processed = pd.concat([X[num_cols], X_encoded], axis=1)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, stratify=y)

# Scale numerical features
scaler = StandardScaler()
X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test[num_cols] = scaler.transform(X_test[num_cols])

# Train XGBoost with class weights
model = XGBClassifier(
    scale_pos_weight=(len(y_train) - sum(y_train)) / sum(y_train),  # Handle imbalance
    eval_metric="auc",
    use_label_encoder=False
)

# Hyperparameter tuning (example)
param_grid = {
    "learning_rate": [0.01, 0.1],
    "max_depth": [3, 5],
    "n_estimators": [100, 200]
}

grid_search = GridSearchCV(model, param_grid, cv=5, scoring="roc_auc")
grid_search.fit(X_train, y_train)

# Evaluate
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
print(f"AUC-ROC: {roc_auc_score(y_test, y_pred)}")
print(f"F1 Score: {f1_score(y_test, y_pred)}")
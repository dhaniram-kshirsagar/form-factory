import pandas as pd
from sklearn.preprocessing import LabelEncoder
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent/"modules/data"/"large-data"/"FoamFactory_V2_27K.csv"
PROCESSED_CSV = Path(__file__).parent/"preprocessed_data.csv"
FEATURES_PATH = Path(__file__).parent/"imp_rev_features.md"
MEAN_VALUES_PATH = Path(__file__).parent/"mean_values.pkl"

# Load the dataset
data = pd.read_csv(CSV_PATH)

# Split the Date column into day, month, and year
data['Date'] = pd.to_datetime(data['Date'])
data['day'] = data['Date'].dt.day
data['month'] = data['Date'].dt.month
data['year'] = data['Date'].dt.year

# Load the important features from imp_rev_features.md
with open(FEATURES_PATH, "r") as file:
    lines = file.readlines()
    important_features = [line.split("|")[1].strip() for line in lines[2:]]  # Skip header and footer

# Prepend month, year, Factory to the important features list
important_features = ['month', 'year', 'Factory'] + important_features

# Select only the important features and the target variable
data = data[important_features + ["Revenue ($)"]]

# Handle categorical columns using LabelEncoder
categorical_columns = data.select_dtypes(include=["object"]).columns
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

means = data.mean(axis=0)
# Save the preprocessed data to a CSV file
#print(means)
data.to_csv(PROCESSED_CSV, index=False)
means.to_csv(MEAN_VALUES_PATH, index=False)
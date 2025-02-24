import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the dataset
data = pd.read_csv("/Users/dhani/foamvenv/smart-data-intelligence/apps/foam_factory/modules/data/large-data/FoamFactory_V2_27K.csv")

# Load the important features from imp_rev_features.md
with open("/Users/dhani/foamvenv/form-factory/imp_rev_features.md", "r") as file:
    lines = file.readlines()
    important_features = [line.split("|")[1].strip() for line in lines[2:]]  # Skip header and footer

# Select only the important features and the target variable
data = data[important_features + ["Revenue ($)"]]

# Handle categorical columns using LabelEncoder
categorical_columns = data.select_dtypes(include=["object"]).columns
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Save the preprocessed data to a CSV file
data.to_csv("/Users/dhani/foamvenv/rev_model/preprocessed_data.csv", index=False)
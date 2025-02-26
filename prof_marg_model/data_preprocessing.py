import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the dataset
data = pd.read_csv("../modules/data/large-data/FoamFactory_V2_27K.csv")

# Split the Date column into day, month, and year
data['Date'] = pd.to_datetime(data['Date'])
data['day'] = data['Date'].dt.day
data['month'] = data['Date'].dt.month
data['year'] = data['Date'].dt.year

# Load the important features from imp_rev_features.md
with open("imp_prof_margin_features.md", "r") as file:
    lines = file.readlines()
    important_features = [line.split("|")[1].strip() for line in lines[2:]]  # Skip header and footer

# Prepend month, year, Factory, and Location to the important features list
important_features = ['month', 'year', 'Factory', 'Location'] + important_features

# Select only the important features and the target variable
data = data[important_features + ["Profit Margin (%)"]]

# Handle categorical columns using LabelEncoder
categorical_columns = data.select_dtypes(include=["object"]).columns
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    print(col)
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

means = data.mean(axis=0)

# Save the preprocessed data to a CSV file
data.to_csv("preprocessed_data.csv", index=False)
means.to_csv("mean_profit_margin_values.csv", index=False)
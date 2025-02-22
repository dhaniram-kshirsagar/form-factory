# After we have cleaned data, let's start building **Prediction Models** to find which is the best for our goals!
# import the required libraries
import json
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

# For ML Modeling
from pycaret.classification import predict_model
# from IPython.display import display, HTML
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, \
    confusion_matrix
from sklearn.feature_selection import SelectKBest, f_classif
from xgboost import XGBClassifier
from collections import Counter
from imblearn.combine import SMOTEENN

plt.style.use('default')

# import warnings
# warnings.filterwarnings("ignore")

# ### Reading data
# load previous cleaned data from Exploratory Data Analysis
df = pd.read_csv('tel_churn_clean.csv')
# Shows the first 5 rows of the DataFrame (default is 5)
df.head()

# remove unnamed column which unnecessary for model
# The 'Unnamed: 0' column often appears when:
# A CSV file was created from a DataFrame that had its index saved
# You read a CSV with index_col parameter not specified in pd.read_csv()
df = df.drop(
    'Unnamed: 0',  # Column name to remove
    axis=1,  # axis=1 means drop column (axis=0 would drop rows)
)

# This is a common step in machine learning preparation where you:
# Separate features (x) from the target variable (Churn)
# Creates a DataFrame with all columns except 'Churn'
# Original DataFrame 'df' remains unchanged since inplace=True wasn't used
x = df.drop(
    'Churn',  # Remove the Churn column
    axis=1  # axis=1 means drop column (axis=0 would drop rows)
)
x

# Seperate the target variable Churn from the ret of the Data Frame
y = df['Churn']
y

# its imbalance dataset
# Check class distribution in target variable, Majority and Minority Class
y.value_counts()  # Shows count of each unique value in y

df['tenure'].min()  # Returns the smallest value in the tenure column

# # Feature Selection
# Selecting only features which has higher correlation with churn
# Assuming x is your feature variables and y is your target (Churn)
# Create the SelectKBest selector
# number of features related to Churn
numberOfFeatures = 7
select_feature = SelectKBest(score_func=f_classif, k=numberOfFeatures)

# Fit and transform the data
# SelectKBest scores measure feature importance. For numerical data, it uses F-test (f_classif) or mutual information (mutual_info_classif) by default.
# Good scores are relative to your dataset - there's no universal threshold. Higher scores indicate stronger relationships with the target variable. Compare scores within your feature set to identify the most important features.
# Key points:
# F-scores: Higher = stronger relationship between feature and target
# Look for significant differences between feature scores
# Consider domain knowledge when interpreting scores
# Use scores to rank features rather than focusing on absolute values
X_selected = select_feature.fit_transform(x, y)

# Get selected feature names
selected_features_mask = select_feature.get_support()
selected_features = x.columns[selected_features_mask]

# Get feature scores
feature_scores = pd.DataFrame({
    'Feature': x.columns,
    'Score': select_feature.scores_
})

# Sort features by score
feature_scores = feature_scores.sort_values('Score', ascending=False)

# Print selected features and their scores
print("Top selected features:")
print(feature_scores.head(numberOfFeatures))

# Create new DataFrame with only selected features
X_new = pd.DataFrame(X_selected, columns=selected_features)
X_new.shape

features = X_new
features = features.set_index(features.columns[0])
#save feature scores to csv
features.to_csv('features.csv')

plt.figure(figsize=(10, 6))
plt.bar(feature_scores['Feature'][:numberOfFeatures], feature_scores['Score'][:numberOfFeatures])
plt.xticks(rotation=45)
plt.title('Top Feature Scores')
plt.tight_layout()
st.pyplot(plt)  # Use st.pyplot() instead of plt.show() for streamlit
plt.clf()  # Clear the figure after displaying

x = x[select_feature.get_feature_names_out()]

# according to the feature selection we have selected 7 top features out of 19 features
# # Train Test Split
# Let's split data into training and validation set in 80:20 ratio

x_train, x_test, y_train, y_test = train_test_split(
    X_new,  # Your feature matrix (with selected features)
    y,  # Your target variable (Churn)
    test_size=0.2,  # 20% of data for testing, 80% for training
    random_state=42  # For reproducible results
)

# show the shape of the train and test data to check the 80/20 split
x_train.shape, y_train.shape, x_test.shape, y_test.shape

plt.figure(figsize=(8, 4))  # Set figure size to 8x4 inches
y.value_counts().plot(
    kind="pie",  # Create a pie chart
    autopct="%1.f%%",  # Show percentages with no decimal places
    labels=["No", "Yes"]  # Labels for the segments (No churn, Yes churn)
)
st.pyplot(plt)  # Use st.pyplot() instead of plt.show()
plt.clf()  # Clear the figure

# We have 2 classes *class 0 and class 1*.
# **class 0 No Churn - majority class**,
# **class 1 Churn -minority class**
# # Need to Fix Imbalance
# Using **Upsampling + ENN** to balanced data before train model

class_counts = Counter(y)
# Create DataFrame for plotting
df = pd.DataFrame({
    'Class': list(class_counts.keys()),
    'Count': list(class_counts.values())
})

# Create bar plot
fig = px.bar(df, x='Class', y='Count', title='Class Distribution Before SMOTE')
st.plotly_chart(fig)
plt.clf()  # Clear the figure

# Print the class distribution before applying SMOTE-ENN
print("Before SMOTE-ENN:", Counter(y))

# Apply SMOTE-ENN : fix imbalanced data
# SMOTEENN combines SMOTE (Synthetic Minority Over-sampling Technique) with ENN (Edited Nearest Neighbors). It:
# Oversamples minority class using SMOTE
# Cleans resulting data using ENN to remove noise
smote = SMOTEENN(random_state=42)
x_st, y_st = smote.fit_resample(x, y)

class_counts = Counter(y_st)
# Create DataFrame for plotting
df = pd.DataFrame({
    'Class': list(class_counts.keys()),
    'Count': list(class_counts.values())
})

# The original dataset had 7043 customer entries with 20 parameters
# We removed 11 Customers because we didnt have the Total Charges for them
# We removed the Customer ID as this is personal
# So shape was reduced to 7032,19
# Due to Churn Imbalance this is now reduced by SMOTE/ENN analysis to 5914,19 and 5914,1 3259 Churn 2655 No Churn
# So we have synthetically created 1390 Churn Customers
# Create bar plot
fig = px.bar(df, x='Class', y='Count', title='Class Distribution After SMOTE')
st.plotly_chart(fig)
plt.clf()  # Clear the figure

# Print the class distribution after applying SMOTE-ENN
print("After SMOTE-ENN:", Counter(y_st))

x_st
y_st

y_st.value_counts()

# since we have performed SMOTEENN (combination of Smote + ENN) sampling method and we can see our dataset is nearly balanced
# ### Now split training and validation set using balanced dataset
x_train, x_test, y_train, y_test = train_test_split(x_st, y_st, test_size=0.2, random_state=42)
x_train.shape, y_train.shape, x_test.shape, y_test.shape

#save training data to csv
train_data = pd.concat([x_train, y_train], axis=1)
train_data.to_csv('final_train_data.csv')
print(train_data.head())

# Building Model with Balanced Dataset and performance hyper parameter tuning using RandomSearchCV

# # Model Training
# In this case, I am using top best 3 model to compare:
# 1. Random Forest Classifier
# 2. XGBoost Classifier
# 3. Gradient Boosting Classifier

# For model evaluation, easier to evaluate

def evaluate_model_performance(model, x_test, y_test):
    prediction = model.predict(x_test)

    # Compute standard classification metrics
    metrics = {
        "accuracy": accuracy_score(y_test, prediction),
        "precision": precision_score(y_test, prediction, average="binary"),  # Change for multi-class
        "recall": recall_score(y_test, prediction, average="binary"),
        "f1_score": f1_score(y_test, prediction, average="binary"),
        "confusion_matrix": confusion_matrix(y_test, prediction).tolist(),
        "classification_report": classification_report(y_test, prediction, output_dict=True)
    }

    # If using a model that supports `predict_proba`, compute log loss
    if hasattr(model, "predict_proba"):
        from sklearn.metrics import log_loss
        probabilities = model.predict_proba(x_test)
        metrics["loss"] = log_loss(y_test, probabilities)

    # Save metrics to JSON
    with open("training_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    print("✅ Training metrics saved to training_metrics.json")

    # Display in Streamlit
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Model Metrics")
        for metric, value in metrics.items():
            if isinstance(value, float):  # Only show numeric metrics
                st.metric(metric.capitalize(), f"{value:.2%}")

    with col2:
        st.subheader("Classification Report")
        st.text(classification_report(y_test, prediction))

        # Confusion Matrix Plot
        fig = plt.figure(figsize=(8, 6))
        sns.heatmap(metrics["confusion_matrix"], annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        st.pyplot(fig)
        plt.clf()  # Clear the figure

def evaluate_model_performance1(model, x_test, y_test):
    prediction = model.predict(x_test)

    col1, col2 = st.columns(2)

    metrics = {
        "Accuracy": accuracy_score(y_test, prediction),
        "Precision": precision_score(y_test, prediction),
        "Recall": recall_score(y_test, prediction),
        "F1 Score": f1_score(y_test, prediction)
    }

    with col1:
        st.subheader("Model Metrics")
        for metric, value in metrics.items():
            st.metric(metric, f"{value:.2%}")

    with col2:
        st.subheader("Classification Report")
        st.text(classification_report(y_test, prediction))

        fig = plt.figure(figsize=(8, 6))
        sns.heatmap(confusion_matrix(y_test, prediction),
                    annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        st.pyplot(fig)
        plt.clf()  # Clear the figure


# ## 1. Random Forest Classifier
# Finding best hyper parameters using Randomized Search CV

param_grid = {
    'n_estimators': [40, 80, 120, 160, 200],  # Number of trees
    'max_depth': [2, 4, 6, 8, 10],  # Tree depth
    'criterion': ['gini'],  # Split criterion
    'random_state': [27, 42, 43]  # Seeds
}

random_search_cv = RandomizedSearchCV(
    estimator=RandomForestClassifier(),
    param_distributions=param_grid,
    n_iter=12,  # Number of parameter settings sampled
    cv=5,  # 5-fold cross-validation
    scoring='f1'  # F1 score optimization
)
random_search_cv.fit(x_train, y_train)

# Get best params as dictionary
best_params = random_search_cv.best_params_
# You could also display it as a table
st.table(pd.DataFrame([best_params]))
st.write(f"Best CV Score: {random_search_cv.best_score_:.4f}")
# print('Best Parameters:', random_search_cv.best_params_)

# Get final model with best param from RandomizedSearchCV
rf_final_model = random_search_cv.best_estimator_

# evaluate Random Forest Classifier
evaluate_model_performance(rf_final_model, x_test, y_test)

# ## 2. XGBoost Classifier
# Finding best hyper parameters using Randomized Search CV

param_grid = {
    'n_estimators': [100, 150, 200, 250, 300],
    'max_depth': [2, 4, 6, 8],
    'learning_rate': [0.001, 0.01, 0.1, 0.2],
    'gamma': [0, 0.1, 0.2, 0.3, 0.4],
    'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.6, 0.7, 0.8, 0.9, 1.0],
    'reg_alpha': [0, 0.1, 0.5, 1.0],
    'reg_lambda': [0, 0.1, 0.5, 1.0],
    'objective': ['binary:logistic']
}

# Create RandomizedSearchCV for XGBoost
RandomizedSearch_xg_cv = RandomizedSearchCV(
    estimator=XGBClassifier(random_state=42),
    param_distributions=param_grid,
    cv=5,
    scoring='accuracy',
    random_state=42
)

# Fit RandomizedSearchCV
RandomizedSearch_xg_cv.fit(x_train, y_train)

# Get best params as dictionary
best_params = RandomizedSearch_xg_cv.best_params_
# You could also display it as a table
st.table(pd.DataFrame([best_params]))
st.write(f"Best CV Score: {RandomizedSearch_xg_cv.best_score_:.4f}")
# print('Best Parameters:', RandomizedSearch_xg_cv.best_params_)

xg_smote_model = RandomizedSearch_xg_cv.best_estimator_

# evaluate Random Forest Classifier
evaluate_model_performance(xg_smote_model, x_test, y_test)

# ## 3. Gradient Boosting Classifier
# Finding best hyper parameters using Randomized Search CV

param_grid = {
    'n_estimators': [100, 150, 200, 250, 300],
    'criterion': ['friedman_mse', 'squared_error', 'mse', 'mae'],
    'max_depth': [2, 4, 6, 8],
    'learning_rate': [0.001, 0.01, 0.1, 0.2],
    'loss': ['deviance', 'exponential']
}

RandomizedSearch_cv = RandomizedSearchCV(
    estimator=GradientBoostingClassifier(random_state=42),
    param_distributions=param_grid,  # Use param_distributions instead of param_grid
    cv=5,
    scoring='accuracy',
    random_state=42
)

RandomizedSearch_cv.fit(x_train, y_train)

# Get best params as dictionary
best_params = RandomizedSearch_cv.best_params_
# You could also display it as a table
st.table(pd.DataFrame([best_params]))
st.write(f"Best CV Score: {RandomizedSearch_cv.best_score_:.4f}")

# print('Best Parameters:', RandomizedSearch_cv.best_params_)

# Pick the best model from the grid spedified
gb_smote_model = RandomizedSearch_cv.best_estimator_

# evaluate Random Forest Classifier
evaluate_model_performance(gb_smote_model, x_test, y_test)

# As we can see, **Gradient Boosting** have slightly better results than **XGBoost**.
# To consider: (first case: GB, second case: XGB)
# 1. **Accuracy**:
#         In the first case, accuracy is 97%, and in the second case, it's 95%. Higher accuracy generally indicates better performance, but it's not the only metric to consider, especially in scenarios with imbalanced classes.
# 2. **Precision**:
#         Precision measures the proportion of true positive predictions among all positive predictions. In the first case, precision is 97%, and in the second case, it's 94%. Higher precision means fewer false positives.
# 3. **Recall**:
#         Recall measures the proportion of true positives that were correctly identified. In the first case, recall is 98%, and in the second case, it's 96%. Higher recall means fewer false negatives.
# 4. **F1 Score**:
#         F1 Score is the harmonic mean of precision and recall. In the first case, it's 97%, and in the second case, it's also 95%. F1 Score provides a balance between precision and recall.
# **Tips:**
# Given these metrics:
# - *If your priority is to minimize false positives (i.e., you want to be very sure that the positive predictions are indeed correct), you might choose the model with higher precision (the first one).*
# - *If your priority is to minimize false negatives (i.e., you want to ensure that as many true positives as possible are identified), you might choose the model with higher recall (the first one).*
# - *If you want a balance between precision and recall, you might consider the F1 Score, in which case both models perform similarly.*
# - *If the classes are imbalanced, consider which metric is more important based on the cost of false positives and false negatives in your specific application.*
# In summary, choose the model based on the specific requirements and priorities of your problem, whether it's optimizing for precision, recall, or finding a balance between the two.
# # Finalizing and Saving Model
# After model evaluation based on matrics aboved,
# we have **Gradient Boosting Model** as the **Final Model**.

from sklearn.ensemble import GradientBoostingClassifier
import joblib

# gb_smote_model = GradientBoostingClassifier(
#   n_estimators=250,     # Number of boosting stages
#   max_depth=8,          # Maximum depth of trees
#   loss='exponential',   # Loss function
#   learning_rate=0.2,    # Shrinks contribution of each tree
#   criterion='friedman_mse'  # Splitting criterion
# )
# Save the Selected Trained Model for loading and making predictions later
joblib.dump(gb_smote_model, 'gradient_boosting_model_new.joblib')
# loaded_model = joblib.load('gradient_boosting_model.joblib')

# Here we go! after we got the final model! Let's create app.py and test it out on Streamlit.
#import the required libraries
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import streamlit as st

plt.style.use('default')

#import warnings
#warnings.filterwarnings("ignore")

# Sample Data Set containing Telco customer data and showing customers left last month into a Panda Data Frame
df = pd.read_csv('TelecomChurn.csv')

# Shows the first 5 rows of the DataFrame (default is 5)
df.head()

# Displays information about the DataFrame including:
# - Total number of entries
# - Column names
# - Number of non-null values in each column
# - Data type of each column
# - Memory usage
#df.info()

# Returns a tuple of (number of rows, number of columns)
#df.shape

# Returns array of column names in the DataFrame
#df.columns.values


# Check columns list and missing values
# df.isnull() Creates a DataFrame of same shape with True where values are null/NaN
# sum() # Sums up the True values (nulls) for each column
#df.isnull().sum()

#check for duplicate records
#df.duplicated() Returns a boolean Series (True for duplicate rows)
#df[df.duplicated()] Creates a DataFrame containing only the duplicate rows
#.shape[0] Gets the number of rows (first element of shape tuple)
#df[df.duplicated()].shape[0]

#check datatype
#int64        Integer column
#float64      Floating point numbers
#object       Usually strings or mixed types
#bool         Boolean (True/False)
#datetime64   Date/time data
#df.dtypes

#since customerId is not required for prediction so drop it
#'customerID' The column name to remove
#axis=1 1 means drop column, 0 would mean drop row
#inplace=True Modifies the DataFrame directly instead of returning a copy
df.drop('customerID',axis=1,inplace=True)

#since total changes is having numerical value but dtype is object to change it into numeric
#'TotalCharges' Column to convert
#errors='coerce' Converts invalid values to NaN
df['TotalCharges']=pd.to_numeric(df['TotalCharges'],errors='coerce')

#print last 5 records of the  dataset
#df.tail(5)

# Only analyze columns with 'object' data type
#df.describe(include =['object'])

# Check the various attributes of data like shape (rows and cols), Columns, datatypes
# Check the descriptive statistics of numeric variables
# Shows the following for each numeric column:
# count - Number of non-null values
# mean  - Average value
# std   - Standard deviation
# min   - Minimum value
# 25%   - First quartile (25th percentile)
# 50%   - Second quartile/median (50th percentile)
# 75%   - Third quartile (75th percentile)
# max   - Maximum value
#df.describe()
# SeniorCitizen is actually a categorical hence the 25%-50%-75% distribution is not 0
# 75% customers have tenure less than 55 months
# Average Monthly charges are USD 64.76 whereas 25% customers pay more than USD 89.85 per month

# Exploratory Data Analysis
#pie chart to count senior citizen
plt.figure(figsize=(10,5))
plt.pie(df["SeniorCitizen"].value_counts(),autopct="%.1f%%",labels=["No","Yes"])
st.pyplot(plt)  # Use st.pyplot() instead of plt.show() for streamlit
plt.clf()       # Clear the figure after displaying
# as we can see 83.8 % of the customers are senior citizen and only 16.2% are adult customer.

#check the distibution of churn class
plt.figure(figsize=(12, 5))  # Set overall figure size
plt.subplot(121)
sns.countplot(data=df, x="Churn")
plt.title("Distribution of Churn")
plt.subplot(122)
df['Churn'].value_counts().plot(kind='pie', autopct="%1.f%%", labels=['No','Yes'])
plt.title('Pie chart of Churn')
plt.tight_layout()
st.pyplot(plt)  # Use st.pyplot() instead of plt.show()
plt.clf()       # Clear the figure

#perentage of each class sample distribution
#print("Customer Churn : {}%".format(np.round((len(df[df["Churn"]=="Yes"])/len(df)*100),decimals=2)))
#print("Customer Not Churn : {}%".format(np.round((len(df[df["Churn"]=="No"])/len(df)*100),decimals=2)))
# as we can see 83.8 % of the customers are senior citizen and only 16.2% are adult customer.

#how much loss we are having because of customer churn
# Convert "TotalCharges" column to numeric
#df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')
churn_customers=df[df["Churn"]=="Yes"]
loss=churn_customers["TotalCharges"].sum()
total_revenue=df["TotalCharges"].sum()
#print("We have lost arround {}$ due to customer churn".format(loss))
#print("We have lost arround {} percentage of revengue due to customer churn".format(np.round(loss/total_revenue*100,decimals=2)))

#plot numerical features with histogram
# Create a figure with 3 subplots in one row
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(18,8))
axes = axs.flatten()  # Convert subplot array to 1D for easier indexing

# List of numeric columns to plot
num_columns=['tenure', 'MonthlyCharges', 'TotalCharges']

# Create histogram for each column
for i, col in enumerate(num_columns):
    if(col!='SeniorCitizen'):  # Skip SeniorCitizen column
        sns.histplot(
            x=col,          # Column to plot
            data=df,        # DataFrame
            hue='Churn',    # Split by Churn status
            ax=axes[i]      # Which subplot to use
        )

fig.tight_layout()  # Adjust spacing between plots
st.pyplot(fig)  # Use st.pyplot() instead of plt.show()
plt.clf()       # Clear the figure

#plot numerical features with boxplot
# Create a figure with 3 subplots in one row
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(16,8))
axes = axs.flatten()  # Convert subplot array to 1D for easier indexing

# List of numeric columns to plot
num_columns=['tenure', 'MonthlyCharges', 'TotalCharges']

# Create box plot for each column
for i, col in enumerate(num_columns):
    if(col!='SeniorCitizen'):  # Skip SeniorCitizen column
        sns.boxplot(
            x=col,          # Column to plot
            data=df,        # DataFrame
            showmeans=True, # Show mean as a point in the box plot
            ax=axes[i]      # Which subplot to use
        )

fig.tight_layout()  # Adjust spacing between plots
st.pyplot(fig)  # Use st.pyplot() instead of plt.show()
plt.clf()       # Clear the figure

# after plotting histogram and boxplot we found that there is no outlier present in numeric dataset so we don't need to do any kind of outlier treatment.
pairplot = sns.pairplot(
    df.drop(columns="SeniorCitizen"),  # DataFrame without SeniorCitizen column
    hue="Churn",                       # Color points based on Churn status
    kind="scatter"                     # Use scatter plots (default)
)
st.pyplot(pairplot)  # Use st.pyplot() instead of plt.show()
plt.clf()           # Clear the figure

# # Univariate Analysis
#plot cateogrical features :
# Get list of categorical columns and adjust it
cat_features = list(df.select_dtypes(include='object').columns)  # Get object (string) columns
cat_features.remove('Churn')                                     # Remove Churn column
cat_features.append('SeniorCitizen')                            # Add SeniorCitizen column

# Calculate grid layout
num_plots = len(cat_features)
num_rows = (num_plots - 1) // 4 + 1  # Integer division to determine rows needed
num_cols = min(num_plots, 4)         # Maximum 4 columns

# Create subplot grid
fig, axs = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(20, 10))
axes = axs.flatten()  # Convert 2D array of axes to 1D for easier indexing

# Create countplot for each categorical feature
for i, col in enumerate(cat_features):
    sns.countplot(
        x=col,          # Categorical feature
        hue="Churn",    # Split by Churn status
        data=df,        # DataFrame
        ax=axes[i]      # Which subplot to use
    )

# Remove empty subplots if any
for j in range(num_plots, len(axes)):
    fig.delaxes(axes[j])

fig.tight_layout()  # Adjust spacing
st.pyplot(fig)  # Use st.pyplot() instead of plt.show()
plt.clf()       # Clear the figure

# # Data Cleaning
#df.isnull() Creates a boolean mask where True = missing value
#.sum() Counts True values (missing values) for each column
df.isnull().sum()

# ### Check Missing Values
# Create DataFrame of missing value percentages
missing = pd.DataFrame(
    (df.isnull().sum())*100/df.shape[0]  # Calculate percentage: (missing count/total rows)*100
).reset_index()  # Convert index (column names) to a column

# Create the plot
plt.figure(figsize=(16,5))  # Set figure size

# Create point plot
ax = sns.pointplot(
    x='index',     # Column names on x-axis
    y=0,           # Percentage values on y-axis (column 0)
    data=missing   # Use the missing values DataFrame
)

# Customize the plot
plt.xticks(
    rotation=90,   # Rotate x-axis labels 90 degrees
    fontsize=7     # Set font size of x-axis labels
)
plt.title("Percentage of Missing values")
plt.ylabel("PERCENTAGE")
st.pyplot(plt)  # Use st.pyplot() instead of plt.show()
plt.clf()       # Clear the figure

# As we can see there are 11 missing values in TotalCharges column. Let's check these records
#df.loc[df ['TotalCharges'].isnull() == True]

# ### Missing Values Treatement
#Removing missing values
# Remove rows with ANY missing values
df.dropna(
    how='any',      # 'any' means drop if ANY column has NaN ('all' means all columns must be NaN)
    inplace=True    # Modify the DataFrame directly instead of returning a copy
)

# Fill remaining missing values with 0
df.fillna(0)       # Note: Without inplace=True, this returns a new DataFrame

# ### Encoding Categorical values into Numeric using Label Encoder
encoder = LabelEncoder()  # Create encoder object

# Loop through columns that have 'object' data type
for feature in df.select_dtypes(include='object').columns:
    # Fit encoder to the column and transform it
    df[feature] = encoder.fit_transform(df[feature])

#show the head and tail encoding into numeric and the numeric type used
#df.head()
#df.tail()
#df.dtypes

#get correlation of churn with other variables
plt.figure(figsize=(16,6))  # Set figure size

# Create correlation bar plot
df.corr()["Churn"].sort_values(ascending=False).plot(kind="bar")
#df.corr()                     # Calculate correlation matrix
#   ["Churn"]                  # Select only correlations with Churn
#   .sort_values(              # Sort correlations
#       ascending=False        # Highest correlations first
#   ).plot(
#       kind="bar"            # Create bar plot
#   )
st.pyplot(plt)  # Use st.pyplot() instead of plt.show()
plt.clf()       # Clear the figure

plt.figure(figsize=(18,9))  # Set figure size

sns.heatmap(
    df.corr(),      # Calculate correlation matrix
    annot=True,     # Show correlation values in cells
    cmap="rainbow"  # Use rainbow color scheme
)
st.pyplot(plt)  # Use st.pyplot() instead of plt.show()
plt.clf()       # Clear the figure

# since we are using ensemble methods for model building so there is no need of feature scaling as its prediction is based on creating multiple decision tree
# # Save Data for Model Building

#save cleaned data to csv
df.to_csv('tel_churn_clean.csv')


# **Let's continue to Model Building**
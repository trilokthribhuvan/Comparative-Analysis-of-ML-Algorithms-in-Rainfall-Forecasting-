# -*- coding: utf-8 -*-
"""RainFall___Prediction_(212).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JGUjnYkgqMDWAR26NeTuAFQyZ26FwF2i

## **Importing the required libraries**
"""

# Surpressing warnings:
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import pandas as pd
import seaborn as sns
from sklearn import preprocessing
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.metrics import jaccard_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score,recall_score,precision_score
import sklearn.metrics as metrics
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

"""### Importing the <a href="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-ML0101EN-SkillUp/labs/ML-FinalAssignment/Weather_Data.csv">Weather Dataset</a>

"""

file_path = '/content/Weather_Data.csv'
df = pd.read_csv(file_path)

df.head()
print(df.info())

class_counts = df['RainTomorrow_Yes'].value_counts()
print(class_counts)
majority_class = class_counts.idxmax()
minority_class = class_counts.idxmin()
print(f"Majority Class: {majority_class}")
print(f"Minority Class: {minority_class}")
imbalance_ratio = class_counts[majority_class] / class_counts[minority_class]
print(f"Imbalance Ratio: {imbalance_ratio}")

df.describe()

"""Describing the data"""

df.dtypes

print(df.isnull().sum())

print(df.columns)

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

df = df.dropna(subset=['Date'])

df['Date'] = df['Date'].apply(lambda x: x.timestamp())

potential_categorical_cols = ['WindGustDir', 'WindDir9am', 'WindDir3pm', 'RainToday', 'RainTomorrow']

categorical_cols = [col for col in potential_categorical_cols if col in df.columns]

df = pd.get_dummies(df, columns=categorical_cols)

df = df.dropna()

target_column = 'RainTomorrow_Yes'  # Replace this with your actual target column name after one-hot encoding
X = df.drop(target_column, axis=1)
y = df[target_column]

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

#the code ensures that if there is a 'Date' column in the DataFrame, its values will be converted to datetime objects, with any unconvertible values set to NaT.
# This is useful for ensuring consistent datetime formatting and handling
# invalid date entries.
if 'Date' in df.columns:
      df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True, errors='coerce')

df_numeric = df.select_dtypes(include=[float, int])

df_numeric = df_numeric.dropna()

df_corr = df_numeric.corr()

print(df_corr)

plt.figure(figsize=(15, 15))
sns.heatmap(df_corr, annot=True, cmap='coolwarm')
plt.show()

"""Preprocessing

### Data Preprocessing
"""

df['Date_Numeric'] = pd.to_numeric(df['Date'])
df = df.drop('Date', axis=1) # Remove the original datetime column

df.replace(['No', 'Yes'], [0,1], inplace=True)
df['RainTomorrow_Yes']

X = df.drop('RainTomorrow_Yes', axis=1)
y = df['RainTomorrow_Yes']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""### KNN

"""

KNN = KNeighborsClassifier(n_neighbors=4)
KNN.fit(X_train, y_train)

predictions = KNN.predict(X_test)

KNN_Accuracy_Score = accuracy_score(y_test, predictions)
KNN_F1_Score = f1_score(y_test, predictions, average='weighted')
KNN_Recall_Score = recall_score(y_test, predictions)
KNN_Precision_Score = precision_score(y_test, predictions)
print('KNN Accuracy Score: ', KNN_Accuracy_Score)
print('KNN F1 Score: ', KNN_F1_Score)
print('KNN Recall Score: ', KNN_Recall_Score)
print('KNN Precision Score: ', KNN_Precision_Score)

"""#Random Forest"""

RF = RandomForestClassifier(n_estimators=100, random_state=42)
RF.fit(X_train, y_train)

predictions =  RF.predict(X_test)

RF_accuracy = accuracy_score(y_test, predictions)
RF_f1 = f1_score(y_test, predictions, average='weighted')
RF_recall = recall_score(y_test, predictions)
RF_precision = precision_score(y_test, predictions)
print('RF Accuracy Score: ', RF_accuracy)
print('RF F1 Score: ', RF_f1)
print('RF Recall Score: ', RF_recall)
print('RF Precision Score: ', RF_precision)

"""#GradientBoosting"""

from sklearn.ensemble import GradientBoostingClassifier
gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
gb.fit(X_train, y_train)
y_pred = gb.predict(X_test)
gb_accuracy = accuracy_score(y_test, y_pred)  # Corrected
gb_f1 = f1_score(y_test, y_pred, average='weighted')  # Corrected
gb_recall = recall_score(y_test, y_pred)  # Corrected
gb_precision = precision_score(y_test, y_pred)  # Corrected
print("GB Accuracy Score:", gb_accuracy)
print("GB F1 Score:", gb_f1)
print("GB Recall:", gb_recall)
print("GB Precision:", gb_precision)

"""## Report

"""

Report = {
    'Classification Algorithm': ['KNN (K=4)', 'Random Forest', 'Gradient Boosting'],  # Corrected
    'Accuracy Score': [KNN_Accuracy_Score, RF_accuracy, gb_accuracy],
    'F1 Score': [KNN_F1_Score, RF_f1, gb_f1],
    'Recall': [KNN_Recall_Score, RF_recall, gb_recall],
    'Precision': [KNN_Precision_Score, RF_precision, gb_precision]
                      }

# Create DataFrame
Report_df = pd.DataFrame(Report)

# Print DataFrame
print(Report_df)

from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=1, cols=1)

# Add Accuracy Score
fig.add_trace(
    go.Bar(
       x=Report['Classification Algorithm'],
       y=Report['Accuracy Score'],
       name='Accuracy Score',
       text=Report['Accuracy Score'],
       textposition='auto'
    ),
    row=1, col=1
)

# Add F1 Score
fig.add_trace(
    go.Bar(
       x=Report['Classification Algorithm'],
       y=Report['F1 Score'],
       name='F1 Score',
       text=Report['F1 Score'],
       textposition='auto'
     ),
     row=1, col=1
)

# Add Recall
fig.add_trace(
   go.Bar(
      x=Report['Classification Algorithm'],
      y=Report['Recall'],
      name='Recall',
      text=Report['Recall'],
      textposition='auto'
      ),
      row=1, col=1
)

# Add Precision
fig.add_trace(
    go.Bar(
       x=Report['Classification Algorithm'],
       y=Report['Precision'],
       name='Precision',
       text=Report['Precision'],
       textposition='auto'
       ),
       row=1, col=1
)

fig.update_yaxes(title_text="Score", row=1, col=1)
fig.update_xaxes(title_text="Classification Algorithm", row=1, col=1)

fig.show()
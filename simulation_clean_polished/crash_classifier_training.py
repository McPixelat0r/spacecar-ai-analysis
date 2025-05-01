# crash_classifier_training.py
"""
Train a classification model to predict CrashOccurred labels using actual feature data.
This replaces DangerScore mimicry with real binary supervised learning.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from imblearn.over_sampling import SMOTE

from models_clean_polished.danger_rating_model_with_angle_weighting import DangerRatingModel

# Step 1: Load crash-labeled dataset
input_path = "../data/cleaned_features_with_crash.csv"
df = pd.read_csv(input_path)

# Step 1b: Add DangerScore column using rule-based model
model = DangerRatingModel()
def compute_danger(row):
    return model.compute(row.to_dict())["DangerScore"]
df["DangerScore"] = df.apply(compute_danger, axis=1)

# Step 2: Select features and target
features = [
    "FOV_Threat_Count",
    "Min_Distance_In_FOV",
    "FOV_Density",
    "FOV_Front_Cone_Threat_Count",
    "Angle_Weighted_Density",
    "Threats_Left_Sector",
    "Threats_Right_Sector",
    "Average_Threat_Angle_Offset",
    "heading_deg",
    "previous_heading_deg",
    "DangerScore"
]
X = df[features]
y = df["CrashOccurred"]

# Step 3: Train/test split (ensure class balance in both sets)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Step 3b: Apply SMOTE oversampling to training set
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# Step 4: Train models with balanced class weights
rf_model = RandomForestClassifier(class_weight='balanced', random_state=42)
rf_model.fit(X_train, y_train)

lr_model = LogisticRegression(class_weight='balanced', max_iter=1000)
lr_model.fit(X_train, y_train)

hgb_model = HistGradientBoostingClassifier(
    class_weight='balanced', max_iter=300, learning_rate=0.1, max_depth=6, random_state=42
)
hgb_model.fit(X_train, y_train)

# Step 4b: Export trained HGB model to file
joblib.dump(hgb_model, "../models_clean_polished/hgb_model.pkl")
print("✅ Trained HGB model saved to '../models_clean_polished/hgb_model.pkl'")

# Step 5: Evaluate
print("Class distribution in dataset:\n", y.value_counts())
print("\nRandom Forest Classifier:\n", classification_report(y_test, rf_model.predict(X_test), zero_division=0))
print("\nLogistic Regression Classifier:\n", classification_report(y_test, lr_model.predict(X_test), zero_division=0))
print("\nHistGradientBoosting Classifier:\n", classification_report(y_test, hgb_model.predict(X_test), zero_division=0))

# Step 6: Plot confusion matrix for RF model
ConfusionMatrixDisplay.from_estimator(
    rf_model, X_test, y_test, display_labels=["No Crash", "Crash"], cmap="Blues"
)
plt.title("Random Forest Confusion Matrix")
plt.tight_layout()
plt.show()

# Step 6b: Plot confusion matrix for Logistic Regression model
ConfusionMatrixDisplay.from_estimator(
    lr_model, X_test, y_test, display_labels=["No Crash", "Crash"], cmap="Oranges"
)
plt.title("Logistic Regression Confusion Matrix")
plt.tight_layout()
plt.show()

# Step 6c: Plot confusion matrix for HistGradientBoostingClassifier
ConfusionMatrixDisplay.from_estimator(
    hgb_model, X_test, y_test, display_labels=["No Crash", "Crash"], cmap="Greens"
)
plt.title("HistGradientBoosting Confusion Matrix")
plt.tight_layout()
plt.show()

# Step 7: Plot feature importances (RF only)
importances = pd.Series(rf_model.feature_importances_, index=features).sort_values()
plt.figure(figsize=(8, 5))
importances.plot(kind='barh')
plt.title("Random Forest Feature Importances (Expanded Features + DangerScore)")
plt.xlabel("Importance")
plt.tight_layout()
plt.show()

# Step 8: Plot Logistic Regression coefficients
lr_coeffs = pd.Series(lr_model.coef_[0], index=features).sort_values()
plt.figure(figsize=(8, 5))
lr_coeffs.plot(kind='barh')
plt.title("Logistic Regression Coefficients")
plt.xlabel("Coefficient Value")
plt.tight_layout()
plt.show()

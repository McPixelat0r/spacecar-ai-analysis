# danger_model_training.py
"""
Trains a regression model to mimic the DangerRatingModel's output (DangerScore).
This serves as a warm-up ML task before using real crash labels.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

from models_clean_polished.danger_rating_model_with_angle_weighting import DangerRatingModel

# Step 1: Load data
input_path = "../data/cleaned_features.csv"
df = pd.read_csv(input_path)

# Step 2: Apply DangerRatingModel to get synthetic DangerScore
model = DangerRatingModel()

def compute_danger(row):
    return model.compute(row.to_dict())["DangerScore"]

df["DangerScore"] = df.apply(compute_danger, axis=1)

# Step 3: Select features and target
features = [
    "FOV_Threat_Count",
    "Min_Distance_In_FOV",
    "FOV_Density",
    "FOV_Front_Cone_Threat_Count",
    "Angle_Weighted_Density"
]
X = df[features]
y = df["DangerScore"]

# Step 4: Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)

# Train Linear Regression model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_preds = lr_model.predict(X_test)

# Step 5: Evaluate both models
print("Random Forest Results:")
print("  MAE:", mean_absolute_error(y_test, rf_preds))
print("  R^2:", r2_score(y_test, rf_preds))

print("\nLinear Regression Results:")
print("  MAE:", mean_absolute_error(y_test, lr_preds))
print("  R^2:", r2_score(y_test, lr_preds))

# Step 6: Plot RF results only (can duplicate for LR if needed)
plt.figure(figsize=(8, 6))
plt.scatter(y_test, rf_preds, alpha=0.5)
plt.plot([0, 1], [0, 1], '--', color='gray')
plt.xlabel("Actual DangerScore")
plt.ylabel("Predicted DangerScore")
plt.title("Random Forest: DangerScore Prediction vs. Actual")
plt.grid(True)
plt.tight_layout()
plt.show()

# Step 7: Plot Linear Regression feature importances
plt.figure(figsize=(8, 5))
coefs = pd.Series(lr_model.coef_, index=features).sort_values()
coefs.plot(kind='barh')
plt.title("Linear Regression: Feature Coefficients")
plt.xlabel("Weight")
plt.grid(True)
plt.tight_layout()
plt.show()

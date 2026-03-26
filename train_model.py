import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import joblib

# -------------------------------
# Load Dataset
# -------------------------------
df = pd.read_csv("data/housing_data.csv")

print("Dataset Loaded Successfully")
print("Shape:", df.shape)

# -------------------------------
# Define Features & Target
# -------------------------------
X = df.drop("price", axis=1)
y = df["price"]

categorical_cols = ["city", "location_type", "furnishing"]

# -------------------------------
# Preprocessing
# -------------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ],
    remainder="passthrough"
)

# -------------------------------
# Improved Random Forest
# -------------------------------
rf = RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", rf)
])

# -------------------------------
# Train-Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print("\nTraining model...")
model.fit(X_train, y_train)

# -------------------------------
# Cross Validation
# -------------------------------
cv_scores = cross_val_score(model, X, y, cv=5, scoring="r2")

# -------------------------------
# Evaluation
# -------------------------------
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nModel Performance:")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2:", round(r2, 4))
print("Cross-Validation R2 Mean:", round(cv_scores.mean(), 4))

# -------------------------------
# Feature Importance
# -------------------------------
feature_names = model.named_steps["preprocessor"].get_feature_names_out()
importances = model.named_steps["regressor"].feature_importances_

feature_importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

print("\nTop 10 Important Features:")
print(feature_importance_df.head(10))

# -------------------------------
# Save Model
# -------------------------------
joblib.dump(model, "models/house_price_model.pkl")

print("\nModel saved successfully!")
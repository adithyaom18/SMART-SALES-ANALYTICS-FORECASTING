import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

import joblib
import os

data_path = "data/processed/forecast_data.csv"
df = pd.read_csv(data_path)

#“I excluded date from features to prevent leakage and used engineered time features instead.”
X = df.drop(columns=["Order Date", "Sales"])
y = df["Sales"]

#“I used chronological splitting to respect time dependency.”
split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test  = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test  = y.iloc[split_index:]

#Train Baseline Model
model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("MAE:", mae)
print("RMSE:", rmse)

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/sales_forecast_model.pkl")

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import joblib

# Prepare features and target
X = df.drop(columns=["Order Date", "Sales"])
y = df["Sales"]

# Train-test split (time-based)
split_index = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]

# Random Forest Model
rf_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=8,
    random_state=42
)

rf_model.fit(X_train, y_train)

# Evaluation
y_pred = rf_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("Random Forest Performance")
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))

# Save model
joblib.dump(rf_model, "models/sales_forecast_rf.pkl")


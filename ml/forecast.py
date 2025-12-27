import pandas as pd
import numpy as np
import joblib

model = joblib.load("models/sales_forecast_model.pkl")

df = pd.read_csv("data/processed/forecast_data.csv")


'''

Predict future monthly sales

Use last known history

Handle lag features correctly

Make it reusable for Flask later

 Key Concept

Forecasting with lag features requires recursive prediction

'''

# Sort data to ensure correct order
df = df.sort_values("Order Date").reset_index(drop=True)

#Now extract the last known values:
last_row = df.iloc[-1]

last_sales = last_row["Sales"]
last_lag_1 = last_row["lag_1"]
last_lag_3 = last_row["lag_3"]
last_rolling = last_row["rolling_3_mean"]

last_date = pd.to_datetime(last_row["Order Date"])

#Decide Forecast Horizon - 3 months
forecast_horizon = 3

#Create Empty List to Store Predictions
future_predictions = []
future_dates = []

#Recursive Forecast Loop
for i in range(forecast_horizon):
    next_month = last_date + pd.DateOffset(months=1)

    month = next_month.month
    year = next_month.year

    input_features = pd.DataFrame([{
        "month": month,
        "year": year,
        "lag_1": last_sales,
        "lag_3": last_lag_3,
        "rolling_3_mean": last_rolling
    }])

    predicted_sales = model.predict(input_features)[0]

    future_predictions.append(predicted_sales)
    future_dates.append(next_month)

    # Update values for next iteration
    last_lag_3 = last_lag_1
    last_lag_1 = last_sales
    last_sales = predicted_sales
    last_rolling = np.mean([last_lag_1, last_lag_3, predicted_sales])
    last_date = next_month

#Create Forecast DataFrame

forecast_df = pd.DataFrame({
    "Order Date": future_dates,
    "Predicted Sales": future_predictions
})

forecast_df

print(forecast_df)

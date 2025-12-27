import pandas as pd
import numpy as np
import joblib

model = joblib.load("models/sales_forecast_model.pkl")

df = pd.read_csv("data/processed/forecast_data.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"])


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

def get_forecast(forecast_horizon=3):
    df_local = df.copy()

    df_local = df_local.sort_values("Order Date").reset_index(drop=True)

    last_row = df_local.iloc[-1]

    last_sales = last_row["Sales"]
    last_lag_1 = last_row["lag_1"]
    last_lag_3 = last_row["lag_3"]
    last_rolling = last_row["rolling_3_mean"]
    last_date = pd.to_datetime(last_row["Order Date"])

    future_predictions = []
    future_dates = []

    for _ in range(forecast_horizon):
        next_month = last_date + pd.DateOffset(months=1)

        input_features = pd.DataFrame([{
            "month": next_month.month,
            "year": next_month.year,
            "lag_1": last_sales,
            "lag_3": last_lag_3,
            "rolling_3_mean": last_rolling
        }])

        predicted_sales = model.predict(input_features)[0]

        future_predictions.append(round(predicted_sales, 2))
        future_dates.append(next_month.strftime("%Y-%m-%d"))

        last_lag_3 = last_lag_1
        last_lag_1 = last_sales
        last_sales = predicted_sales
        last_rolling = np.mean([last_lag_1, last_lag_3, predicted_sales])
        last_date = next_month

    return {
        "dates": future_dates,
        "predicted_sales": future_predictions
    }

def get_actual_vs_predicted(last_n_months=6):
    df_local = df.copy()
    df_local = df_local.sort_values("Order Date").reset_index(drop=True)

    # Take last N rows
    actual_df = df_local.tail(last_n_months)

    X_actual = actual_df.drop(columns=["Order Date", "Sales"])
    actual_sales = actual_df["Sales"].values
    dates = pd.to_datetime(actual_df["Order Date"]).dt.strftime("%Y-%m-%d").values

    predicted_sales = model.predict(X_actual)

    return {
        "dates": dates.tolist(),
        "actual_sales": actual_sales.round(2).tolist(),
        "predicted_sales": predicted_sales.round(2).tolist()
    }

def get_kpis():
    # Load RAW data for analytics
    raw_df = pd.read_csv("data/raw/Super store Sales.csv")

    raw_df["Order Date"] = pd.to_datetime(raw_df["Order Date"], dayfirst=True)

    # Total Sales
    total_sales = round(raw_df["Sales"].sum(), 2)

    # Monthly aggregation
    monthly_sales = (
        raw_df
        .set_index("Order Date")
        .resample("M")["Sales"]
        .sum()
    )

    avg_monthly_sales = round(monthly_sales.mean(), 2)

    # Best Category
    best_category = (
        raw_df
        .groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    # Peak Month
    peak_month = monthly_sales.idxmax().strftime("%B %Y")

    return {
        "total_sales": total_sales,
        "avg_monthly_sales": avg_monthly_sales,
        "best_category": best_category,
        "peak_month": peak_month
    }

def get_analytics_data():
    raw_df = pd.read_csv("data/raw/Super store Sales.csv")
    raw_df["Order Date"] = pd.to_datetime(raw_df["Order Date"], dayfirst=True)

    # Monthly Sales
    monthly = (
        raw_df
        .set_index("Order Date")
        .resample("M")["Sales"]
        .sum()
        .reset_index()
    )

    # Category Sales
    category_sales = (
        raw_df
        .groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    # Region Sales
    region_sales = (
        raw_df
        .groupby("Region")["Sales"]
        .sum()
    )

    return {
        "monthly": {
            "dates": monthly["Order Date"].dt.strftime("%Y-%m").tolist(),
            "sales": monthly["Sales"].round(2).tolist()
        },
        "category": {
            "labels": category_sales.index.tolist(),
            "sales": category_sales.round(2).tolist()
        },
        "region": {
            "labels": region_sales.index.tolist(),
            "sales": region_sales.round(2).tolist()
        }
    }



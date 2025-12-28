import pandas as pd
import numpy as np
import joblib

# Load trained model once
model = joblib.load("models/sales_forecast_model.pkl")


# --------------------------------------------------
# INTERNAL HELPER: Load & Prepare Monthly Data
# --------------------------------------------------
def _load_monthly_data(active_dataset_path=None):

    if active_dataset_path:
        df = pd.read_csv(active_dataset_path)
    else:
        df = pd.read_csv("data/raw/Super store Sales.csv")

    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

    monthly = (
        df
        .set_index("Order Date")
        .resample("M")["Sales"]
        .sum()
        .reset_index()
    )

    # Feature engineering
    monthly["month"] = monthly["Order Date"].dt.month
    monthly["year"] = monthly["Order Date"].dt.year
    monthly["lag_1"] = monthly["Sales"].shift(1)
    monthly["lag_3"] = monthly["Sales"].shift(3)
    monthly["rolling_3_mean"] = monthly["Sales"].rolling(3).mean()

    monthly = monthly.dropna().reset_index(drop=True)

    return monthly


# --------------------------------------------------
# FORECAST FUTURE SALES
# --------------------------------------------------
def get_forecast(active_dataset_path=None, forecast_horizon=3):

    df_local = _load_monthly_data(active_dataset_path)
    df_local = df_local.sort_values("Order Date").reset_index(drop=True)

    last_row = df_local.iloc[-1]

    last_sales = last_row["Sales"]
    last_lag_1 = last_row["lag_1"]
    last_lag_3 = last_row["lag_3"]
    last_rolling = last_row["rolling_3_mean"]
    last_date = last_row["Order Date"]

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

        # Recursive update
        last_lag_3 = last_lag_1
        last_lag_1 = last_sales
        last_sales = predicted_sales
        last_rolling = np.mean([last_lag_1, last_lag_3, predicted_sales])
        last_date = next_month

    return {
        "dates": future_dates,
        "predicted_sales": future_predictions
    }


# --------------------------------------------------
# ACTUAL vs PREDICTED (MODEL EVALUATION)
# --------------------------------------------------
def get_actual_vs_predicted(active_dataset_path=None, last_n_months=6):

    df_local = _load_monthly_data(active_dataset_path)
    df_local = df_local.sort_values("Order Date").reset_index(drop=True)

    actual_df = df_local.tail(last_n_months)

    X_actual = actual_df[["month", "year", "lag_1", "lag_3", "rolling_3_mean"]]
    actual_sales = actual_df["Sales"].values
    dates = actual_df["Order Date"].dt.strftime("%Y-%m-%d").values

    predicted_sales = model.predict(X_actual)

    return {
        "dates": dates.tolist(),
        "actual_sales": actual_sales.round(2).tolist(),
        "predicted_sales": predicted_sales.round(2).tolist()
    }


# --------------------------------------------------
# KPIs
# --------------------------------------------------
def get_kpis(active_dataset_path=None):

    if active_dataset_path:
        df = pd.read_csv(active_dataset_path)
    else:
        df = pd.read_csv("data/raw/Super store Sales.csv")

    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df = df.dropna(subset=["Order Date", "Sales"])

    monthly_sales = (
        df
        .set_index("Order Date")
        .resample("M")["Sales"]
        .sum()
        .reset_index()
    )

    if monthly_sales.empty:
        return {
            "total_sales": 0,
            "avg_monthly_sales": 0,
            "peak_month": "N/A",
            "growth_pct": 0,
            "data_coverage": 0
        }

    total_sales = monthly_sales["Sales"].sum()
    avg_monthly_sales = monthly_sales["Sales"].mean()

    peak_idx = monthly_sales["Sales"].idxmax()
    peak_month = monthly_sales.loc[peak_idx]["Order Date"].strftime("%B %Y")

    if len(monthly_sales) >= 2 and monthly_sales.iloc[-2]["Sales"] != 0:
        last = monthly_sales.iloc[-1]["Sales"]
        prev = monthly_sales.iloc[-2]["Sales"]
        growth_pct = ((last - prev) / prev) * 100
    else:
        growth_pct = 0

    data_coverage = len(monthly_sales)

    # ✅ Convert ALL values to native Python types
    return {
        "total_sales": float(round(total_sales, 2)),
        "avg_monthly_sales": float(round(avg_monthly_sales, 2)),
        "peak_month": str(peak_month),
        "growth_pct": float(round(growth_pct, 2)),
        "data_coverage": int(data_coverage)
    }


# --------------------------------------------------
# ANALYTICS DATA
# --------------------------------------------------
def get_analytics_data(active_dataset_path=None):

    if active_dataset_path:
        raw_df = pd.read_csv(active_dataset_path)
    else:
        raw_df = pd.read_csv("data/raw/Super store Sales.csv")

    raw_df["Order Date"] = pd.to_datetime(raw_df["Order Date"], errors="coerce")

    response = {}

    # Monthly sales (always exists)
    monthly = (
        raw_df
        .set_index("Order Date")
        .resample("M")["Sales"]
        .sum()
        .reset_index()
    )

    response["monthly"] = {
        "dates": monthly["Order Date"].dt.strftime("%Y-%m").tolist(),
        "sales": monthly["Sales"].round(2).tolist()
    }

    # Category-wise (optional)
    if "Category" in raw_df.columns:
        category = raw_df.groupby("Category")["Sales"].sum().reset_index()
        response["category"] = {
            "labels": category["Category"].tolist(),
            "sales": category["Sales"].round(2).tolist()
        }

    # Region-wise (optional)
    if "Region" in raw_df.columns:
        region = raw_df.groupby("Region")["Sales"].sum().reset_index()
        response["region"] = {
            "labels": region["Region"].tolist(),
            "sales": region["Sales"].round(2).tolist()
        }

    return response


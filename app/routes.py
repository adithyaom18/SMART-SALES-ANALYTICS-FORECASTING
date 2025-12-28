from flask import (
    Blueprint,
    jsonify,
    render_template,
    redirect,
    url_for,
    request,
    session
)

import os
import pandas as pd

from ml.forecast import (
    get_forecast,
    get_actual_vs_predicted,
    get_kpis,
    get_analytics_data
)



main = Blueprint("main", __name__)


@main.route("/")
def home():
    return redirect(url_for("main.index"))


@main.route("/forecast", methods=["GET"])
def forecast():
    horizon = request.args.get("months", default=3, type=int)
    active_dataset = session.get("active_dataset")
    result = get_forecast(active_dataset, horizon)
    return jsonify(result)



@main.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@main.route("/index")
def index():
    return render_template("index.html")

@main.route("/evaluation", methods=["GET"])
def evaluation():
    active_dataset = session.get("active_dataset")
    result = get_actual_vs_predicted(active_dataset, last_n_months=6)
    return jsonify(result)


@main.route("/forecast-view")
def forecast_view():
    return render_template("forecast.html")

@main.route("/kpis", methods=["GET"])
def kpis():
    active_dataset = session.get("active_dataset")
    return jsonify(get_kpis(active_dataset))


@main.route("/analytics-data", methods=["GET"])
def analytics_data():
    active_dataset = session.get("active_dataset")
    return jsonify(get_analytics_data(active_dataset))



from flask import send_from_directory
import os

@main.route("/debug-css")
def debug_css():
    return send_from_directory(
        os.path.join(os.getcwd(), "app/static/css"),
        "dashboard.css"
    )


@main.route("/upload-dataset", methods=["POST"])
def upload_dataset():
    if "dataset" not in request.files:
        return "No file part", 400

    file = request.files["dataset"]

    if file.filename == "":
        return "No selected file", 400

    if not file.filename.lower().endswith(".csv"):
        return "Only CSV files are allowed", 400

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    upload_folder = os.path.join(BASE_DIR, "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    # 🔥 READ CSV COLUMNS
    df = pd.read_csv(file_path)
    columns = df.columns.tolist()

    # Send columns to mapping page
    return render_template(
        "column_mapping.html",
        columns=columns,
        filename=file.filename
    )

@main.route("/map-columns", methods=["POST"])
def map_columns():
    filename = request.form.get("filename")
    date_col = request.form.get("date_column")
    sales_col = request.form.get("sales_column")
    category_col = request.form.get("category_column")
    region_col = request.form.get("region_column")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    upload_path = os.path.join(BASE_DIR, "uploads", filename)

    df = pd.read_csv(upload_path)

    # Mandatory mappings
    df = df.rename(columns={
        date_col: "Order Date",
        sales_col: "Sales"
    })

    # Optional mappings
    if category_col:
        df = df.rename(columns={category_col: "Category"})

    if region_col:
        df = df.rename(columns={region_col: "Region"})

    # Clean data
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df = df.dropna(subset=["Order Date", "Sales"])

    processed_dir = os.path.join(BASE_DIR, "data", "uploaded_processed")
    os.makedirs(processed_dir, exist_ok=True)

    processed_path = os.path.join(processed_dir, "processed_" + filename)
    df.to_csv(processed_path, index=False)

    # Activate dataset
    session["active_dataset"] = processed_path

    return redirect(url_for("main.dashboard"))



@main.route("/reset-dataset")
def reset_dataset():
    session.pop("active_dataset", None)
    return redirect(url_for("main.dashboard"))


@main.route("/active-dataset")
def active_dataset():
    dataset_path = session.get("active_dataset")

    if not dataset_path:
        return jsonify({"name": "Default Dataset"})

    return jsonify({"name": os.path.basename(dataset_path)})


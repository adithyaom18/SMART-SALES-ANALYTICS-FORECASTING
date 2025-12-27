from ml.forecast import get_forecast
from flask import Blueprint, jsonify
from flask import render_template
from flask import redirect, url_for
from ml.forecast import get_actual_vs_predicted
from flask import request
from ml.forecast import get_kpis
from ml.forecast import get_analytics_data


main = Blueprint("main", __name__)


@main.route("/")
def home():
    return redirect(url_for("main.index"))


@main.route("/forecast", methods=["GET"])
def forecast():
    horizon = request.args.get("months", default=3, type=int)
    result = get_forecast(forecast_horizon=horizon)
    return jsonify(result)


@main.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@main.route("/index")
def index():
    return render_template("index.html")

@main.route("/evaluation", methods=["GET"])
def evaluation():
    result = get_actual_vs_predicted(last_n_months=6)
    return jsonify(result)

@main.route("/forecast-view")
def forecast_view():
    return render_template("forecast.html")

@main.route("/kpis", methods=["GET"])
def kpis():
    return jsonify(get_kpis())

@main.route("/analytics-data", methods=["GET"])
def analytics_data():
    return jsonify(get_analytics_data())


from flask import send_from_directory
import os

@main.route("/debug-css")
def debug_css():
    return send_from_directory(
        os.path.join(os.getcwd(), "app/static/css"),
        "dashboard.css"
    )

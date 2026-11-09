from pathlib import Path

import charts
from flask import Flask, render_template, request

from data import INDICATORS, TransportData

BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "panel.csv"

data = TransportData(DATA_PATH)

app = Flask(__name__)


@app.route("/")
def index():
    first_year, last_year = data.year_range()
    n_countries = len(data.countries())
    return f"{n_countries} countries, {first_year}-{last_year}"


@app.route("/countries")
def countries():
    return data.countries()


@app.route("/test")
def test():
    year_data = data.one_year(2024)
    return charts.scatter_chart(year_data)


@app.route("/explore")
def explore():
    first_year, last_year = data.year_range()

    selected = request.args.getlist("country") or ["PT", "ES", "FR", "DE", "NO"]

    indicator = request.args.get("indicator", "emission_pc")
    if indicator not in INDICATORS:
        indicator = "emission_pc"

    start = request.args.get("start", default=first_year, type=int)
    end = request.args.get("end", default=last_year, type=int)

    rows = data.filter(selected, start, end)
    chart = charts.line_chart(rows, indicator)
    stats = data.key_stats(rows, indicator)

    return render_template(
        "explore.html",
        countries=data.countries(),
        indicators=INDICATORS,
        selected=selected,
        indicator=indicator,
        start=start,
        end=end,
        first_year=first_year,
        last_year=last_year,
        chart=chart,
        stats=stats,
    )

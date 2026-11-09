from pathlib import Path

import charts
from flask import Flask, render_template, request

from data import INDICATORS, TransportData

FINDINGS = ["TODO: add key findings here"]

BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "panel.csv"

data = TransportData(DATA_PATH)

app = Flask(__name__)


@app.route("/")
def index():
    first_year, last_year = data.year_range()
    year_data = data.one_year(last_year)

    return render_template(
        "index.html",
        latest_year=last_year,
        stats=data.key_stats(data.df, "emission_pc"),
        trend_chart=charts.trend_chart(
            data.yearly_average("emission_pc"), "emission_pc"
        ),
        ranking_chart=charts.bar_chart(year_data, "emission_pc"),
        scatter_chart=charts.scatter_chart(data.df),
        findings=FINDINGS,
    )


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

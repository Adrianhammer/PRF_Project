from pathlib import Path

import charts
from flask import Flask, render_template, request

from data import INDICATORS, TransportData

FINDINGS = [    "Wealth drives motorisation, but the effect flattens out. Above about "
    "€57,000 GDP per capita, more income no longer adds cars.",

    "Older fleets mean more cars. Ten percentage points more cars over ten "
    "years add 66 cars per 1,000 inhabitants.",

    "The vehicle stock is the main driver of emissions. 100 more cars per "
    "1,000 inhabitants add 0.28 tonnes of CO₂ per capita, about 13% of the "
    "average.",

    "At the same vehicle stock, richer countries emit less. Income raises "
    "emissions through the number of cars, and lowers them through efficiency.",

    "Fleet age lowers emissions, so it measures how much people drive rather "
    "than vehicle technology. Old fleets stand still.",

    "Transport emissions fell 14% in 2020 and never returned to the "
    "pre-pandemic level. 2024 is still 13% below 2019.",

    "Luxembourg is excluded. Fuel sold to drivers from neighbouring countries "
    "distorts both emissions and GDP per capita.",
]

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

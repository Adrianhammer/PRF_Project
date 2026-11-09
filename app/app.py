from pathlib import Path

import charts
from flask import Flask

from data import TransportData

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
